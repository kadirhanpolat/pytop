"""High-level TDA pipeline that composes filtration, reduction, and analysis.

``TDAPipeline`` is an immutable builder: each method returns a new instance
with updated state.  This lets you write concise multi-step analyses::

    from pytop.tda_pipeline import TDAPipeline

    # Rips filtration → standard Z/2 reduction → barcode
    pipe = TDAPipeline.from_points(pts).rips(max_dimension=2).reduce()
    bars = pipe.barcode(dimension=1)

    # Čech filtration → cohomology reduction → diagram
    pipe = TDAPipeline.from_points(pts).cech(max_scale=1.5).reduce("cohomology")
    diag = pipe.diagram()

    # Multi-prime torsion detection
    results = TDAPipeline.from_points(pts).rips(max_dimension=2).compare_primes([2, 3, 5])

Public API
----------
TDAPipeline        — main pipeline class
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

from .cech_complex import cech_filtration
from .persistence_distances import (
    PersistenceLandscape,
    bottleneck_distance,
    persistence_entropy,
    wasserstein_distance,
)
from .persistence_distances import (
    persistence_landscape as _persistence_landscape,
)
from .persistent_homology import (
    FilteredComplex,
    PersistencePair,
    persistence_pairs,
    vietoris_rips_filtration,
)
from .persistent_homology import (
    barcode as _barcode,
)
from .persistent_homology import (
    persistence_diagram as _diagram,
)
from .persistent_homology_fp import is_prime, persistence_pairs_fp
from .persistent_homology_optimized import (
    persistence_pairs_cohomology,
    persistence_pairs_twist,
)

# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TDAPipeline:
    """Immutable TDA pipeline.  Build it step by step; each call returns a new
    instance with updated state.

    Typical workflow::

        pipe = (
            TDAPipeline.from_points(pts)
            .rips(max_dimension=2, max_scale=2.0)
            .reduce(method="twist")
        )
        essential_h1 = [p for p in pipe.pairs() if p.is_essential and p.dimension == 1]

    Attributes
    ----------
    filtered : FilteredComplex | None
        The filtration, once built.
    computed_pairs : tuple[PersistencePair, ...] | None
        The persistence pairs, once reduced.
    """

    filtered: FilteredComplex | None = field(default=None)
    computed_pairs: tuple[PersistencePair, ...] | None = field(default=None)

    # ------------------------------------------------------------------ #
    # Constructors                                                         #
    # ------------------------------------------------------------------ #

    @classmethod
    def from_points(cls, points: Sequence[Sequence[float]]) -> TDAPipeline:
        """Create a pipeline from a raw point cloud.

        Call ``.rips()`` or ``.cech()`` next to build the filtration.

        Parameters
        ----------
        points : Sequence[Sequence[float]]
            A finite point cloud in R^d.
        """
        return cls()

    @classmethod
    def from_filtration(cls, filtered: FilteredComplex) -> TDAPipeline:
        """Create a pipeline from a pre-built :class:`.FilteredComplex`.

        Skip filtration and call ``.reduce()`` directly.
        """
        return cls(filtered=filtered)

    # ------------------------------------------------------------------ #
    # Filtration step                                                      #
    # ------------------------------------------------------------------ #

    def rips(
        self,
        points: Sequence[Sequence[float]] | None = None,
        *,
        max_dimension: int = 1,
        max_scale: float | None = None,
    ) -> TDAPipeline:
        """Build a Vietoris-Rips filtration.

        Parameters
        ----------
        points :
            The point cloud.  Required if this pipeline was created with
            ``TDAPipeline()`` or ``TDAPipeline.from_points(pts)`` (pass
            ``pts`` here in the latter case, or pass it to ``from_points``
            and call ``rips()`` without arguments — but then ``points`` must
            be stored elsewhere; passing it again here is simpler and safer).
        max_dimension :
            Maximum simplex dimension.
        max_scale :
            Truncate filtration at this scale.
        """
        if points is None:
            raise ValueError(
                "points must be supplied to .rips() when building from a point cloud."
            )
        fc = vietoris_rips_filtration(
            _PointSpace(points), max_dimension=max_dimension, max_scale=max_scale
        )
        return TDAPipeline(filtered=fc, computed_pairs=None)

    def cech(
        self,
        points: Sequence[Sequence[float]] | None = None,
        *,
        max_dimension: int = 1,
        max_scale: float | None = None,
    ) -> TDAPipeline:
        """Build a Čech filtration.

        Parameters
        ----------
        points :
            The point cloud.
        max_dimension :
            Maximum simplex dimension.
        max_scale :
            Truncate at this circumradius.
        """
        if points is None:
            raise ValueError(
                "points must be supplied to .cech() when building from a point cloud."
            )
        fc = cech_filtration(points, max_dimension=max_dimension, max_scale=max_scale)
        return TDAPipeline(filtered=fc, computed_pairs=None)

    # ------------------------------------------------------------------ #
    # Reduction step                                                       #
    # ------------------------------------------------------------------ #

    def reduce(
        self,
        method: str = "standard",
        prime: int = 2,
        *,
        include_zero_persistence: bool = False,
    ) -> TDAPipeline:
        """Run the persistence reduction.

        Parameters
        ----------
        method :
            One of ``"standard"`` (Z/2 XOR), ``"twist"`` (Twist+Clearing),
            ``"cohomology"`` (de Silva dual), ``"fp"`` (Z/p, requires ``prime``).
        prime :
            The field characteristic for ``method="fp"``.  Must be prime.
            Ignored for other methods.
        include_zero_persistence :
            Whether to include zero-length bars.

        Returns
        -------
        TDAPipeline
            New pipeline with :attr:`computed_pairs` populated.

        Raises
        ------
        RuntimeError
            If no filtration has been built yet.
        ValueError
            If ``method`` is unrecognised, or if ``prime`` is not prime
            when ``method="fp"``.
        """
        if self.filtered is None:
            raise RuntimeError(
                "No filtration available.  Call .rips() or .cech() first, "
                "or use TDAPipeline.from_filtration(fc)."
            )
        fc = self.filtered
        kw: dict[str, Any] = {"include_zero_persistence": include_zero_persistence}

        if method == "standard":
            pairs = persistence_pairs(fc, **kw)
        elif method == "twist":
            pairs = persistence_pairs_twist(fc, **kw)
        elif method == "cohomology":
            pairs = persistence_pairs_cohomology(fc, **kw)
        elif method == "fp":
            if not is_prime(prime):
                raise ValueError(f"prime must be a prime integer ≥ 2, got {prime!r}.")
            pairs = persistence_pairs_fp(fc, prime=prime, **kw)
        else:
            raise ValueError(
                f"Unknown reduction method {method!r}.  "
                "Choose from: 'standard', 'twist', 'cohomology', 'fp'."
            )

        return TDAPipeline(filtered=fc, computed_pairs=pairs)

    # ------------------------------------------------------------------ #
    # Multi-prime analysis                                                 #
    # ------------------------------------------------------------------ #

    def compare_primes(
        self,
        primes: Sequence[int] = (2, 3, 5),
        *,
        include_zero_persistence: bool = False,
    ) -> dict[int, tuple[PersistencePair, ...]]:
        """Run reduction for multiple prime fields and return a dict.

        Useful for detecting Z-homology torsion: if the Betti numbers differ
        between two primes, torsion classes are present.

        Parameters
        ----------
        primes :
            Sequence of prime integers to use as field characteristics.
        include_zero_persistence :
            Passed to each reduction.

        Returns
        -------
        dict[int, tuple[PersistencePair, ...]]
            Maps each prime to its persistence pairs.
        """
        if self.filtered is None:
            raise RuntimeError(
                "No filtration available. Call .rips(), .cech(), or "
                "use TDAPipeline.from_filtration(fc) first."
            )
        return {
            p: persistence_pairs_fp(
                self.filtered,
                prime=p,
                include_zero_persistence=include_zero_persistence,
            )
            for p in primes
        }

    # ------------------------------------------------------------------ #
    # Output / analysis                                                    #
    # ------------------------------------------------------------------ #

    def pairs(
        self, dimension: int | None = None
    ) -> tuple[PersistencePair, ...]:
        """Return persistence pairs, optionally restricted to one dimension.

        Raises
        ------
        RuntimeError
            If reduction has not been run yet.
        """
        self._require_pairs()
        assert self.computed_pairs is not None
        if dimension is None:
            return self.computed_pairs
        return tuple(p for p in self.computed_pairs if p.dimension == dimension)

    def barcode(
        self, dimension: int | None = None
    ) -> tuple[tuple[float, float], ...]:
        """Return ``(birth, death)`` bars.

        Parameters
        ----------
        dimension :
            If given, restrict to this homological degree.
        """
        self._require_pairs()
        assert self.computed_pairs is not None
        return _barcode(self.computed_pairs, dimension=dimension)

    def diagram(self) -> dict[int, tuple[tuple[float, float], ...]]:
        """Return persistence diagram grouped by dimension."""
        self._require_pairs()
        assert self.computed_pairs is not None
        return _diagram(self.computed_pairs)

    def landscape(
        self,
        dimension: int = 0,
        k: int = 1,
        num_points: int = 100,
    ) -> PersistenceLandscape:
        """Return the k-th persistence landscape for dimension ``dimension``.

        Parameters
        ----------
        dimension :
            Homological degree.
        k :
            Landscape rank (1-indexed).
        num_points :
            Number of grid points.
        """
        self._require_pairs()
        assert self.computed_pairs is not None
        return _persistence_landscape(
            self.computed_pairs,
            degree=dimension,
            num_layers=k,
            num_grid_points=num_points,
        )

    def entropy(self, dimension: int | None = None) -> float:
        """Return persistence entropy (Shannon entropy of bar lengths).

        Parameters
        ----------
        dimension :
            If given, restrict to this degree before computing entropy.
        """
        self._require_pairs()
        assert self.computed_pairs is not None
        return persistence_entropy(self.computed_pairs, degree=dimension)

    def bottleneck(
        self,
        other: TDAPipeline | tuple[PersistencePair, ...],
        dimension: int | None = None,
    ) -> float:
        """Bottleneck distance to ``other``'s persistence pairs.

        Parameters
        ----------
        other :
            Another :class:`TDAPipeline` (must have pairs) or a raw
            ``tuple[PersistencePair, ...]``.
        dimension :
            Restrict both barcodes to this degree before computing.
        """
        self._require_pairs()
        assert self.computed_pairs is not None
        a_pairs = self.pairs(dimension)
        if isinstance(other, TDAPipeline):
            other._require_pairs()
            assert other.computed_pairs is not None
            b_pairs = other.pairs(dimension)
        else:
            b_pairs = tuple(pp for pp in other if dimension is None or pp.dimension == dimension)
        return bottleneck_distance(a_pairs, b_pairs)

    def wasserstein(
        self,
        other: TDAPipeline | tuple[PersistencePair, ...],
        p: float = 1.0,
        dimension: int | None = None,
    ) -> float:
        """p-Wasserstein distance to ``other``'s persistence pairs."""
        self._require_pairs()
        assert self.computed_pairs is not None
        a_pairs = self.pairs(dimension)
        if isinstance(other, TDAPipeline):
            other._require_pairs()
            assert other.computed_pairs is not None
            b_pairs = other.pairs(dimension)
        else:
            b_pairs = tuple(pp for pp in other if dimension is None or pp.dimension == dimension)
        return wasserstein_distance(a_pairs, b_pairs, p=p)

    def summary(self) -> str:
        """Return a human-readable summary of the pipeline state."""
        lines: list[str] = ["TDAPipeline"]
        if self.filtered is not None:
            fc = self.filtered
            dim_counts: dict[int, int] = {}
            for d in fc.dimensions:
                dim_counts[d] = dim_counts.get(d, 0) + 1
            dims_str = ", ".join(
                f"dim {d}: {n}" for d, n in sorted(dim_counts.items())
            )
            lines.append(f"  filtration: {fc.size()} simplices ({dims_str})")
        else:
            lines.append("  filtration: (not yet built)")

        if self.computed_pairs is not None:
            pairs = self.computed_pairs
            dim_counts_p: dict[int, int] = {}
            for pp in pairs:
                dim_counts_p[pp.dimension] = dim_counts_p.get(pp.dimension, 0) + 1
            essential = [pp for pp in pairs if pp.is_essential]
            dims_str_p = ", ".join(
                f"H_{d}: {n}" for d, n in sorted(dim_counts_p.items())
            )
            lines.append(f"  pairs: {len(pairs)} ({dims_str_p})")
            ess_str = ", ".join(
                f"H_{d}: {sum(1 for e in essential if e.dimension == d)}"
                for d in sorted({e.dimension for e in essential})
            )
            lines.append(f"  essential: {len(essential)} ({ess_str or 'none'})")
        else:
            lines.append("  pairs: (not yet reduced)")

        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    # Internal                                                             #
    # ------------------------------------------------------------------ #

    def _require_pairs(self) -> None:
        if self.computed_pairs is None:
            raise RuntimeError(
                "No persistence pairs available.  Call .reduce() first."
            )


# ---------------------------------------------------------------------------
# Private space adapter
# ---------------------------------------------------------------------------


class _PointSpace:
    """Adapts a flat point list to the metric-space protocol used by
    vietoris_rips_filtration."""

    def __init__(self, pts: Sequence[Sequence[float]]) -> None:
        self._pts: list[tuple[float, ...]] = [tuple(float(x) for x in p) for p in pts]

    @property
    def carrier(self) -> list[tuple[float, ...]]:
        return self._pts

    def distance_between(self, a: tuple[float, ...], b: tuple[float, ...]) -> float:
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
