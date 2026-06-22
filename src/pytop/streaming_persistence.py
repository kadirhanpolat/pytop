"""Online / streaming persistence — incremental barcode update.

:class:`StreamingPersistence` maintains the standard Z/2 column reduction
incrementally: simplices are inserted one at a time (in non-decreasing
filtration order) and the reduced boundary matrix is extended by one column
per insertion.  This lets you update the barcode without recomputing from
scratch when new simplices arrive.

The internal representation mirrors the Twist+Clearing bitmask layout
(each column is a Python bigint).  The GIL is held throughout; the class is
not thread-safe.

Pure Python, no dependencies.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .persistent_homology import PersistencePair

__all__ = [
    "StreamingPersistence",
]


@dataclass
class StreamingPersistence:
    """Incremental persistence computation via online Z/2 column reduction.

    Usage
    -----
    ::

        sp = StreamingPersistence()
        sp.add_simplex((0,), 0.0)         # vertex 0, born at ε=0
        sp.add_simplex((1,), 0.0)         # vertex 1
        sp.add_simplex((0, 1), 1.0)       # edge, born at ε=1
        pairs = sp.current_pairs()        # [(dim=0, birth=0, death=1)]
        betti = sp.current_betti()        # {0: 1}  (one H0 class survives)

    Simplices **must** be inserted in non-decreasing birth order with all
    faces inserted before their cofaces (the standard filtration condition).
    """

    # --- public (read-only after construction) ---
    _simplex_to_idx: dict[tuple[int, ...], int] = field(default_factory=dict, repr=False)
    _columns: list[int] = field(default_factory=list, repr=False)
    _births: list[float] = field(default_factory=list, repr=False)
    _dims: list[int] = field(default_factory=list, repr=False)
    # pivot row → column index that "owns" that pivot
    _low_inverse: dict[int, int] = field(default_factory=dict, repr=False)
    # (creator_idx, destroyer_idx) pairs from the reduction
    _raw_pairs: list[tuple[int, int]] = field(default_factory=list, repr=False)

    # ------------------------------------------------------------------
    # Insertion
    # ------------------------------------------------------------------

    def add_simplex(
        self,
        simplex: tuple[int, ...] | list[int],
        birth: float,
    ) -> None:
        """Insert ``simplex`` at filtration value ``birth``.

        All faces of ``simplex`` must have been inserted previously and with
        birth ≤ ``birth`` (standard filtration ordering).

        Parameters
        ----------
        simplex:
            Vertex indices (any iterable of ints; sorted canonically).
        birth:
            Filtration birth value.
        """
        key = tuple(sorted(simplex))
        if key in self._simplex_to_idx:
            raise ValueError(f"Simplex {key} has already been inserted.")

        idx = len(self._columns)
        self._simplex_to_idx[key] = idx
        self._births.append(birth)
        dim = len(key) - 1
        self._dims.append(dim)

        # Build boundary column: XOR in face indices
        col: int = 0
        if dim > 0:
            for k in range(len(key)):
                face = key[:k] + key[k + 1 :]
                face_idx = self._simplex_to_idx.get(face)
                if face_idx is None:
                    raise ValueError(
                        f"Face {face} of simplex {key} has not been inserted yet."
                    )
                col ^= 1 << face_idx

        # Standard Z/2 column reduction
        while col:
            p = col.bit_length() - 1
            if p not in self._low_inverse:
                self._low_inverse[p] = idx
                break
            col ^= self._columns[self._low_inverse[p]]

        self._columns.append(col)

        if col:
            # col reduced to a nonzero column → (creator p, destroyer idx)
            p = col.bit_length() - 1
            self._raw_pairs.append((p, idx))

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def current_pairs(self, *, include_zero_persistence: bool = False) -> list[PersistencePair]:
        """Return all finite persistence pairs accumulated so far.

        Parameters
        ----------
        include_zero_persistence:
            If *True*, include pairs with ``birth == death``.

        Returns
        -------
        list[PersistencePair]
        """
        pairs: list[PersistencePair] = []
        for creator, destroyer in self._raw_pairs:
            b = self._births[creator]
            d = self._births[destroyer]
            if not include_zero_persistence and b == d:
                continue
            pairs.append(
                PersistencePair(
                    dimension=self._dims[creator],
                    birth=b,
                    death=d,
                )
            )
        return pairs

    def current_betti(self) -> dict[int, int]:
        """Return the Betti numbers (counts of essential classes) at each dimension.

        An essential class is a simplex whose column reduced to zero and was
        never paired as a *creator* by any later simplex.

        Returns
        -------
        dict[int, int]
            Mapping ``dimension → count`` for all dimensions with nonzero Betti
            number.  Dimensions not present have Betti number 0.
        """
        # Creator indices from finite pairs (these are the "positive" simplices
        # that paired with a destroyer).
        paired_creators: set[int] = {c for c, _ in self._raw_pairs}

        betti: dict[int, int] = {}
        for idx, col in enumerate(self._columns):
            # A "positive" simplex has its reduced column equal to 0.
            if col == 0 and idx not in paired_creators:
                d = self._dims[idx]
                betti[d] = betti.get(d, 0) + 1
        return betti

    def current_essential_pairs(self) -> list[PersistencePair]:
        """Return essential (infinite) persistence pairs — classes that never die.

        Returns
        -------
        list[PersistencePair]
            Each pair has ``death = math.inf``.
        """
        paired_creators: set[int] = {c for c, _ in self._raw_pairs}
        result: list[PersistencePair] = []
        for idx, col in enumerate(self._columns):
            if col == 0 and idx not in paired_creators:
                result.append(
                    PersistencePair(
                        dimension=self._dims[idx],
                        birth=self._births[idx],
                        death=math.inf,
                    )
                )
        return result

    def num_simplices(self) -> int:
        """Return the number of simplices inserted so far."""
        return len(self._columns)
