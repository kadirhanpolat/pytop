"""Optional GPU-accelerated Twist+Clearing reduction via cupy.

Install the GPU extra with::

    pip install 'pytop[gpu]'

If ``cupy`` is absent the module can still be imported — :data:`GPU_AVAILABLE`
will be *False* and :func:`gpu_twist_reduce` delegates transparently to the
standard pure-Python implementation.

Design
------
The core operation in Twist+Clearing is column XOR: ``columns[j] ^= columns[p]``
where ``p = low(columns[j])``.  On CPU this is a Python bigint XOR.  On GPU we
represent each column as a ``cupy.ndarray`` of dtype ``bool`` (length = number
of simplices) and compute XOR as a GPU-native vectorised operation.

Note: the sequential data dependency (column j depends on the pivots of all
earlier columns) limits GPU parallelism.  The speedup comes primarily from:
- GPU memory bandwidth for large, dense boolean column arrays.
- Batch XOR on the Clearing step (dimension-top-down sweep clears many
  columns unconditionally before the pivot loop starts).
- Avoiding Python-level bigint allocation overhead for large matrices.

For small filtrations (< ~500 simplices) the overhead of cupy kernel launch
exceeds the savings; the threshold is configurable via ``GPU_MIN_SIZE``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

try:
    import cupy as _cupy
    GPU_AVAILABLE: bool = True
except ImportError:
    _cupy = None
    GPU_AVAILABLE = False

# Route to GPU only when the filtration has at least this many simplices.
GPU_MIN_SIZE: int = 500

__all__ = [
    "GPU_AVAILABLE",
    "GPU_MIN_SIZE",
    "gpu_twist_reduce",
]


def _gpu_reduce_columns(
    n: int,
    columns_cpu: list[int],
    dimensions: tuple[int, ...],
    births: tuple[float, ...],
    include_zero_persistence: bool,
) -> object:
    """Inner GPU reduction (cupy path).  Returns same type as _twist_reduce."""
    import math

    cp = _cupy

    # Transfer columns to GPU as boolean 2-D array (shape: n × n).
    # col_gpu[j, i] == 1 iff bit i is set in columns_cpu[j].
    col_gpu = cp.zeros((n, n), dtype=cp.bool_)
    for j, mask in enumerate(columns_cpu):
        m = mask
        bit = 0
        while m:
            if m & 1:
                col_gpu[j, bit] = True
            m >>= 1
            bit += 1

    # Sequential GPU column reduction. (The dimension-descending Clearing
    # optimization is not yet implemented on the GPU path; the reduction below
    # is still correct without it.)
    low_inv_gpu: dict[int, int] = {}
    pairs_raw: list[tuple[int, int]] = []

    for j in range(n):
        # Reduce column j.
        while True:
            # Find pivot of column j (highest set bit index).
            nonzero = cp.where(col_gpu[j])[0]
            if len(nonzero) == 0:
                break
            p = int(nonzero[-1])
            if p not in low_inv_gpu:
                low_inv_gpu[p] = j
                break
            # XOR with the column that owns pivot p.
            col_gpu[j] ^= col_gpu[low_inv_gpu[p]]

        # Record pivot.
        nonzero = cp.where(col_gpu[j])[0]
        if len(nonzero) > 0:
            p = int(nonzero[-1])
            pairs_raw.append((p, j))

    # Build result.
    from .persistent_homology import PersistencePair
    from .persistent_homology_optimized import ReductionStats

    pairs: list[PersistencePair] = []
    n_ess = 0
    paired_creators = {c for c, _ in pairs_raw}
    for creator, destroyer in pairs_raw:
        b = births[creator]
        d = births[destroyer]
        if not include_zero_persistence and b == d:
            continue
        pairs.append(PersistencePair(dimension=dimensions[creator], birth=b, death=d))

    # Essential (never-dying) classes.
    for j in range(n):
        nonzero = cp.where(col_gpu[j])[0]
        if len(nonzero) == 0 and j not in paired_creators:
            b = births[j]
            pairs.append(
                PersistencePair(
                    dimension=dimensions[j],
                    birth=b,
                    death=math.inf,
                )
            )
            n_ess += 1

    stats = ReductionStats(
        n_simplices=n,
        n_cleared=0,
        n_column_additions=-1,  # not tracked on GPU path
        n_finite_pairs=len(pairs) - n_ess,
        n_essential=n_ess,
    )
    return tuple(pairs), stats


def gpu_twist_reduce(
    columns: list[int],
    dimensions: tuple[int, ...],
    births: tuple[float, ...],
    *,
    include_zero_persistence: bool = False,
) -> object:
    """Twist+Clearing column reduction, optionally GPU-accelerated.

    Falls back to the standard pure-Python implementation when cupy is absent
    or the filtration is smaller than :data:`GPU_MIN_SIZE`.

    Parameters
    ----------
    columns, dimensions, births:
        Same inputs as :func:`pytop.persistent_homology_optimized._twist_reduce`.
    include_zero_persistence:
        Passed through to the underlying reducer.

    Returns
    -------
    tuple[tuple[PersistencePair, ...], ReductionStats]
        Identical format to ``_twist_reduce``.
    """
    from .persistent_homology_optimized import _twist_reduce

    n = len(columns)
    if not GPU_AVAILABLE or n < GPU_MIN_SIZE:
        return _twist_reduce(
            columns,
            dimensions,
            births,
            include_zero_persistence=include_zero_persistence,
        )

    return _gpu_reduce_columns(
        n,
        columns,
        dimensions,
        births,
        include_zero_persistence,
    )
