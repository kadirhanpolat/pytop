"""Catalog of named topological spaces.

SpaceCatalog is a queryable registry of SpaceRecord objects.  Each record
pairs metadata (canonical name, aliases, known Boolean properties, optional
pi-base ID) with a constructor that returns a live TopologicalSpace instance.

Usage::

    from pytop.space_catalog import catalog

    # Retrieve a record by name or alias
    rec = catalog.get("Sorgenfrey line")
    space = rec.build()          # returns a TopologicalSpace instance

    # Query by properties
    results = catalog.search(compact=True, hausdorff=False)
    for rec in results:
        print(rec.name)

    # List everything
    all_records = catalog.list_all()

To register additional spaces::

    from pytop.space_catalog import catalog, SpaceRecord
    catalog.register(SpaceRecord(name="My space", ...))
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from .spaces import TopologicalSpace


@dataclass
class SpaceRecord:
    """Metadata and constructor for a single named topological space.

    Parameters
    ----------
    name:
        Canonical name (used for lookup).
    description:
        One-sentence mathematical description.
    properties:
        Known Boolean topological properties.  Keys use lowercase snake_case
        (e.g. ``"hausdorff"``, ``"compact"``, ``"first_countable"``).
        A missing key means the property is unknown / not recorded, not False.
    constructor:
        Callable returning a TopologicalSpace instance.  May be None for
        spaces not yet implemented.
    aliases:
        Alternative names accepted by :meth:`SpaceCatalog.get`.
    pi_base_id:
        Identifier in the pi-base database (e.g. ``"S000009"``), if known.
    """

    name: str
    description: str
    properties: dict[str, bool]
    constructor: Callable[[], TopologicalSpace] | None = None
    aliases: list[str] = field(default_factory=list)
    pi_base_id: str | None = None

    def build(self) -> TopologicalSpace:
        """Return a fresh TopologicalSpace instance for this space."""
        if self.constructor is None:
            raise NotImplementedError(f"No constructor registered for {self.name!r}")
        return self.constructor()


class SpaceCatalog:
    """Queryable registry of SpaceRecord objects."""

    def __init__(self, records: list[SpaceRecord] | None = None) -> None:
        self._records: list[SpaceRecord] = list(records or [])

    def register(self, record: SpaceRecord) -> None:
        """Add a SpaceRecord to the catalog."""
        self._records.append(record)

    def list_all(self) -> list[SpaceRecord]:
        """Return all registered records."""
        return list(self._records)

    def get(self, name: str) -> SpaceRecord | None:
        """Return the record matching *name* (canonical or alias), or None."""
        key = name.strip().lower()
        for rec in self._records:
            if rec.name.lower() == key:
                return rec
            if any(a.lower() == key for a in rec.aliases):
                return rec
        return None

    def search(self, **props: bool) -> list[SpaceRecord]:
        """Return records matching all specified Boolean properties.

        Pass property names as keyword arguments::

            catalog.search(compact=True, hausdorff=False)

        Only records that have the property recorded AND match the value are
        included.  Records that do not mention a property are excluded.
        """
        return [
            rec for rec in self._records
            if all(rec.properties.get(k) == v for k, v in props.items())
        ]

    def __len__(self) -> int:
        return len(self._records)

    def __repr__(self) -> str:
        return f"SpaceCatalog({len(self._records)} spaces)"


# ---------------------------------------------------------------------------
# Default catalog — populated from named_spaces
# ---------------------------------------------------------------------------

def _build_default_catalog() -> SpaceCatalog:
    from . import named_spaces as ns

    records: list[SpaceRecord] = [
        SpaceRecord(
            name="Sierpiński space",
            description="Two-point space {0,1} with topology {∅,{1},{0,1}}.",
            properties={
                "t0": True, "t1": False, "hausdorff": False,
                "compact": True, "connected": True, "path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": False,
            },
            constructor=ns.sierpinski_space,
            aliases=["sierpinski"],
            pi_base_id="S000003",
        ),
        SpaceRecord(
            name="Cofinite topology on N",
            description="Cofinite topology on the natural numbers.",
            properties={
                "t0": True, "t1": True, "hausdorff": False,
                "compact": True, "connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": False,
            },
            constructor=ns.cofinite_topology_on_naturals,
            aliases=["cofinite on naturals", "cofinite topology on omega"],
        ),
        SpaceRecord(
            name="Cofinite topology on R",
            description="Cofinite topology on the real numbers.",
            properties={
                "t0": True, "t1": True, "hausdorff": False,
                "compact": True, "connected": True,
                "first_countable": False, "second_countable": False, "separable": True,
                "lindelof": True, "metrizable": False,
            },
            constructor=ns.cofinite_topology_on_reals,
            aliases=["cofinite on reals"],
        ),
        SpaceRecord(
            name="Cocountable topology on R",
            description="Cocountable topology on the real numbers.",
            properties={
                "t0": True, "t1": True, "hausdorff": False,
                "compact": False, "connected": True, "lindelof": True,
                "first_countable": False, "second_countable": False,
                "metrizable": False,
            },
            constructor=ns.cocountable_topology_on_reals,
            aliases=["cocountable on reals"],
        ),
        SpaceRecord(
            name="Real line",
            description="R with the standard Euclidean topology.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": True, "sigma_compact": True,
                "connected": True, "path_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.real_line,
            aliases=["R", "real numbers", "standard real line"],
        ),
        SpaceRecord(
            name="Sorgenfrey line",
            description="R with lower limit topology generated by half-open intervals [a,b).",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": False,
                "connected": False, "path_connected": False, "locally_connected": False,
                "totally_disconnected": True, "zero_dimensional": True,
                "first_countable": True, "second_countable": False, "separable": True,
                "lindelof": True, "metrizable": False,
            },
            constructor=ns.sorgenfrey_line,
            aliases=["lower limit topology", "lower limit line"],
            pi_base_id="S000009",
        ),
        SpaceRecord(
            name="Rational numbers",
            description="Q with the subspace topology from R.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": False,
                "connected": False, "path_connected": False,
                "totally_disconnected": True, "zero_dimensional": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.rational_numbers,
            aliases=["Q", "rationals"],
        ),
        SpaceRecord(
            name="Irrational numbers",
            description="R\\Q with the subspace topology from R.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": False,
                "connected": False, "path_connected": False,
                "totally_disconnected": True, "zero_dimensional": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.irrational_numbers,
            aliases=["irrationals", "R minus Q"],
        ),
        SpaceRecord(
            name="Cantor set",
            description="Standard middle-thirds Cantor set in [0,1] with subspace topology.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": False, "path_connected": False,
                "totally_disconnected": True, "zero_dimensional": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.cantor_set,
            aliases=["Cantor space"],
        ),
        SpaceRecord(
            name="Hilbert cube",
            description="Countably infinite product of [0,1] with the product topology.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True,
                "connected": True, "path_connected": True, "locally_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.hilbert_cube,
            aliases=["[0,1]^omega"],
        ),
        SpaceRecord(
            name="Long line",
            description="omega_1 x [0,1) with lexicographic order topology.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": True,
                "connected": True, "path_connected": True, "locally_connected": True,
                "first_countable": True, "second_countable": False, "separable": False,
                "lindelof": False, "metrizable": False, "paracompact": False,
            },
            constructor=ns.long_line,
            aliases=["long ray"],
        ),
        SpaceRecord(
            name="Topologist's sine curve",
            description="Closure of {(x, sin(1/x)) : x > 0} in R².",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True,
                "connected": True, "path_connected": False,
                "locally_connected": False, "locally_path_connected": False,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.topologists_sine_curve,
            aliases=["closed topologist's sine curve"],
        ),
        SpaceRecord(
            name="Comb space",
            description="Horizontal base, vertical spine, and teeth at 1/n in R².",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True,
                "connected": True, "path_connected": False,
                "locally_connected": False,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.comb_space,
        ),
        SpaceRecord(
            name="Warsaw circle",
            description="Closed topologist's sine curve joined by an arc.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True,
                "connected": True, "path_connected": False,
                "locally_connected": False,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.warsaw_circle,
        ),
        SpaceRecord(
            name="Infinite broom",
            description="Union of segments from (0,0) to (1, 1/n) for n≥1 and to (1,0).",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True,
                "connected": True, "path_connected": True,
                "locally_connected": False,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.infinite_broom,
        ),
        SpaceRecord(
            name="Moore plane",
            description="Upper half-plane with tangent-disk neighborhoods at x-axis points.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": False,
                "compact": False, "locally_compact": False,
                "first_countable": True, "second_countable": False, "separable": True,
                "lindelof": False, "metrizable": False, "paracompact": False,
            },
            constructor=ns.moore_plane,
            aliases=["Niemytzki plane", "Niemytzki space"],
            pi_base_id="S000008",
        ),
        SpaceRecord(
            name="Arens-Fort space",
            description="N×N; all points isolated except (0,0) whose neighborhoods are cofinite per column.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": False,
                "first_countable": False, "second_countable": False, "separable": True,
                "sequential": False,
            },
            constructor=ns.arens_fort_space,
            pi_base_id="S000007",
        ),
        SpaceRecord(
            name="Fort space",
            description="One-point compactification of discrete N.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True,
                "connected": False, "totally_disconnected": True, "zero_dimensional": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.fort_space,
            aliases=["one-point compactification of N", "convergent sequence space"],
        ),
        # ── Batch 2 ──────────────────────────────────────────────────────────
        SpaceRecord(
            name="Discrete countable space",
            description="Natural numbers N with the discrete topology.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": True,
                "connected": False, "totally_disconnected": True, "zero_dimensional": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.discrete_countable_space,
            aliases=["N discrete", "discrete N"],
        ),
        SpaceRecord(
            name="Particular point topology on N",
            description="Topology on N where U is open iff 0∈U (or U=∅).",
            properties={
                "t0": True, "t1": False, "hausdorff": False,
                "compact": False, "connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
            },
            constructor=ns.particular_point_topology_on_naturals,
            aliases=["particular point topology on naturals"],
        ),
        SpaceRecord(
            name="Excluded point topology on N",
            description="Topology on N where U is open iff 0∉U or U=N.",
            properties={
                "t0": True, "t1": False, "hausdorff": False,
                "compact": False, "connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
            },
            constructor=ns.excluded_point_topology_on_naturals,
            aliases=["excluded point topology on naturals"],
        ),
        SpaceRecord(
            name="Double origin topology",
            description="Real line with a second copy of 0; each origin's neighborhoods exclude the other.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": False, "normal": False,
                "compact": False, "locally_compact": True,
                "connected": True, "path_connected": True, "locally_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": False,
            },
            constructor=ns.double_origin_topology,
            aliases=["line with two origins"],
            pi_base_id="S000010",
        ),
        SpaceRecord(
            name="Michael line",
            description="R with irrationals as isolated points; rationals retain standard topology.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": False,
                "first_countable": True, "second_countable": False, "separable": False,
                "lindelof": False,
            },
            constructor=ns.michael_line,
        ),
        SpaceRecord(
            name="Tychonoff plank",
            description="(omega_1+1) x (omega+1) with the product of order topologies.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True,
                "connected": True,
                "first_countable": False, "second_countable": False, "separable": False,
                "metrizable": False,
            },
            constructor=ns.tychonoff_plank,
        ),
        SpaceRecord(
            name="Deleted Tychonoff plank",
            description="Tychonoff plank minus the corner point (omega_1, omega).",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": False, "normal": False,
                "compact": False,
                "second_countable": False, "separable": False,
                "metrizable": False,
            },
            constructor=ns.deleted_tychonoff_plank,
        ),
        SpaceRecord(
            name="Stone-Čech compactification of N",
            description="The Stone-Cech compactification beta_N of the discrete space N.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "extremally_disconnected": True,
                "connected": False, "totally_disconnected": True, "zero_dimensional": True,
                "first_countable": False, "second_countable": False, "separable": True,
                "metrizable": False,
            },
            constructor=ns.stone_cech_compactification_of_N,
            aliases=["beta N", "betaN", "Stone-Cech compactification of N"],
        ),
        SpaceRecord(
            name="Furstenberg topology",
            description="Z with basis {a + bZ : b >= 1}; arithmetic progressions are clopen.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False,
                "connected": False, "totally_disconnected": True, "zero_dimensional": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.furstenberg_topology,
            aliases=["evenly spaced integer topology", "arithmetic progression topology"],
        ),
        SpaceRecord(
            name="Pseudo-arc",
            description="Hereditarily indecomposable chainable compact connected metrizable space.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True,
                "connected": True, "path_connected": False,
                "locally_connected": False, "locally_path_connected": False,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.pseudo_arc,
        ),
        # ── Batch 3 ──────────────────────────────────────────────────────────
        SpaceRecord(
            name="Unit interval",
            description="Closed unit interval [0,1] with subspace topology from R.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": True, "path_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "simply_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.unit_interval,
            aliases=["[0,1]", "closed unit interval"],
        ),
        SpaceRecord(
            name="Unit circle",
            description="S^1 = {(x,y) in R^2 : x^2 + y^2 = 1} with subspace topology.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": True, "path_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "simply_connected": False,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.unit_circle,
            aliases=["S^1", "circle"],
        ),
        SpaceRecord(
            name="Closed unit disk",
            description="D^2 = {(x,y) in R^2 : x^2+y^2 <= 1} with subspace topology.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": True, "path_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "simply_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.closed_unit_disk,
            aliases=["D^2", "disk"],
        ),
        SpaceRecord(
            name="Torus",
            description="T^2 = S^1 x S^1 with the product topology.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": True, "path_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "simply_connected": False,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.torus,
            aliases=["T^2", "T2"],
        ),
        SpaceRecord(
            name="Cantor cube",
            description="Countably infinite product of the discrete two-point space {0,1}.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": False, "path_connected": False,
                "totally_disconnected": True, "zero_dimensional": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.cantor_cube,
            aliases=["{0,1}^omega", "2^omega"],
        ),
        SpaceRecord(
            name="Baire space",
            description="Countably infinite product of the discrete space N; homeomorphic to the irrationals.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": False,
                "connected": False, "path_connected": False,
                "totally_disconnected": True, "zero_dimensional": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.baire_space,
            aliases=["omega^omega", "N^omega"],
        ),
        SpaceRecord(
            name="Lexicographic square",
            description="[0,1]^2 with lexicographic order topology.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "normal": True,
                "compact": True,
                "connected": True,
                "first_countable": True, "second_countable": False, "separable": False,
                "metrizable": False,
            },
            constructor=ns.lexicographic_square,
            aliases=["lex square"],
        ),
        SpaceRecord(
            name="One-point compactification of R",
            description="R union {inf} with the one-point compactification topology; homeomorphic to S^1.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": True, "path_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.one_point_compactification_of_reals,
            aliases=["R union {inf}", "Alexandroff extension of R"],
        ),
        SpaceRecord(
            name="Cantor fan",
            description="Cone over the Cantor set; quotient of C x [0,1] collapsing C x {0} to the apex.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True,
                "connected": True, "path_connected": True,
                "locally_connected": False, "locally_path_connected": False,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.cantor_fan,
        ),
        SpaceRecord(
            name="Knaster-Kuratowski fan",
            description="Cantor-based fan in R^2; connected with apex, totally disconnected without it.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False,
                "connected": True, "path_connected": False,
                "locally_connected": False,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.knaster_kuratowski_fan,
            aliases=["Cantor's teepee"],
        ),
        SpaceRecord(
            name="Hilbert space",
            description="Separable Hilbert space l^2 of square-summable sequences.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": False,
                "connected": True, "path_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.hilbert_space,
            aliases=["l^2", "ell_2"],
        ),
        SpaceRecord(
            name="p-adic integers",
            description="p-adic integers Z_p with the p-adic metric topology.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": False, "path_connected": False,
                "totally_disconnected": True, "zero_dimensional": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.p_adic_integers,
            aliases=["Z_p"],
        ),
        # ── Batch 4 ──────────────────────────────────────────────────────────
        SpaceRecord(
            name="Half-open interval",
            description="Half-open interval [0,1) with subspace topology from R.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": True,
                "connected": True, "path_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.half_open_interval,
            aliases=["[0,1)"],
        ),
        SpaceRecord(
            name="Open interval",
            description="Open unit interval (0,1) with subspace topology from R; homeomorphic to R.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": True,
                "connected": True, "path_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.open_interval,
            aliases=["(0,1)"],
        ),
        SpaceRecord(
            name="Half-open real line",
            description="Half-open ray [0, inf) with subspace topology from R.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": True,
                "connected": True, "path_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "simply_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.half_open_real_line,
            aliases=["[0,inf)", "half-line"],
        ),
        SpaceRecord(
            name="Real projective plane",
            description="RP^2 = S^2 / (x ~ -x); compact non-orientable 2-manifold.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": True, "path_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "simply_connected": False,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.real_projective_plane,
            aliases=["RP^2", "RP2"],
        ),
        SpaceRecord(
            name="Klein bottle",
            description="Compact non-orientable surface without boundary.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": True, "path_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "simply_connected": False,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.klein_bottle,
            aliases=["K"],
        ),
        SpaceRecord(
            name="Möbius band",
            description="[0,1]x[0,1] with (0,t)~(1,1-t); compact non-orientable with boundary.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": True, "path_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "simply_connected": False,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.mobius_band,
            aliases=["Mobius band", "Mobius strip"],
        ),
        SpaceRecord(
            name="Dunce hat",
            description="Contractible quotient of a disk; not locally contractible at the singular vertex.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": True, "path_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "simply_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.dunce_hat,
        ),
        SpaceRecord(
            name="Hawaiian earring",
            description="Union of circles of radius 1/n tangent to the origin; not semi-locally simply connected.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": True, "path_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "simply_connected": False,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.hawaiian_earring,
        ),
        SpaceRecord(
            name="omega_1",
            description="First uncountable ordinal [0, omega_1) with the order topology.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": True,
                "connected": True,
                "first_countable": True, "second_countable": False, "separable": False,
                "lindelof": False, "metrizable": False,
            },
            constructor=ns.omega_1,
            aliases=["first uncountable ordinal", "[0, omega_1)"],
        ),
        SpaceRecord(
            name="omega_1 + 1",
            description="Successor ordinal space [0, omega_1] with the order topology.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True,
                "connected": True,
                "first_countable": False, "second_countable": False, "separable": False,
                "metrizable": False,
            },
            constructor=ns.omega_1_plus_1,
            aliases=["[0, omega_1]"],
        ),
        SpaceRecord(
            name="Stone-Čech remainder",
            description="Stone-Cech remainder beta_N \\ N; compact, extremally disconnected, not separable.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True,
                "connected": False, "totally_disconnected": True, "zero_dimensional": True,
                "first_countable": False, "second_countable": False, "separable": False,
                "metrizable": False, "extremally_disconnected": True,
            },
            constructor=ns.stone_cech_remainder,
            aliases=["N*", "beta_N minus N"],
        ),
        SpaceRecord(
            name="One-point compactification of Q",
            description="One-point compactification of Q; compact, T1, connected, not Hausdorff.",
            properties={
                "t0": True, "t1": True, "hausdorff": False,
                "regular": False,
                "compact": True,
                "connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": False,
            },
            constructor=ns.one_point_compactification_of_Q,
            aliases=["Q union {inf}"],
        ),
        # ── Batch 5 ──────────────────────────────────────────────────────────
        SpaceRecord(
            name="Real plane",
            description="R^2 with the standard Euclidean topology.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": True,
                "connected": True, "path_connected": True, "simply_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.real_plane,
            aliases=["R^2", "Euclidean plane"],
        ),
        SpaceRecord(
            name="Punctured plane",
            description="R^2 minus the origin; homotopy equivalent to S^1.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": True,
                "connected": True, "path_connected": True, "simply_connected": False,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.punctured_plane,
            aliases=["R^2 \\ {0}", "plane minus origin"],
        ),
        SpaceRecord(
            name="2-sphere",
            description="S^2 = {x in R^3 : |x| = 1} with subspace topology.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": True, "path_connected": True, "simply_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.two_sphere,
            aliases=["S^2", "sphere"],
        ),
        SpaceRecord(
            name="3-sphere",
            description="S^3 = {x in R^4 : |x| = 1} with subspace topology.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": True, "path_connected": True, "simply_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.three_sphere,
            aliases=["S^3"],
        ),
        SpaceRecord(
            name="Sierpinski carpet",
            description="Fractal subset of [0,1]^2; universal compact planar locally connected continuum.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True,
                "connected": True, "path_connected": True, "simply_connected": False,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.sierpinski_carpet,
        ),
        SpaceRecord(
            name="Menger curve",
            description="Universal compact metrizable 1-dimensional locally connected continuum.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True,
                "connected": True, "path_connected": True, "simply_connected": False,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.menger_curve,
        ),
        SpaceRecord(
            name="Open cylinder",
            description="R x S^1 with the product topology.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": True,
                "connected": True, "path_connected": True, "simply_connected": False,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.open_cylinder,
            aliases=["R x S^1"],
        ),
        SpaceRecord(
            name="Tube",
            description="Closed cylinder S^1 x [0,1] with product topology.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": True, "path_connected": True, "simply_connected": False,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.tube,
            aliases=["S^1 x [0,1]", "closed cylinder"],
        ),
        SpaceRecord(
            name="Open topologist's sine curve",
            description="Graph of sin(1/x) for x > 0; homeomorphic to R.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": True,
                "connected": True, "path_connected": True, "simply_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.open_topologists_sine_curve,
            aliases=["graph of sin(1/x)"],
        ),
        SpaceRecord(
            name="Erdős space",
            description="Subspace of l^2 with rational coordinates; totally disconnected, dim = 1.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "normal": True,
                "compact": False, "locally_compact": False,
                "connected": False, "totally_disconnected": True,
                "zero_dimensional": False,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.erdos_space,
            aliases=["E", "rational l^2"],
        ),
        SpaceRecord(
            name="Complete Erdős space",
            description="Subspace of l^2 with irrational coordinates; completely metrizable, dim = 1.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "normal": True,
                "compact": False, "locally_compact": False,
                "connected": False, "totally_disconnected": True,
                "zero_dimensional": False,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.complete_erdos_space,
            aliases=["E_c", "irrational l^2"],
        ),
        # ── Batch 6 ──────────────────────────────────────────────────────────
        SpaceRecord(
            name="R^n",
            description="Euclidean n-space R^n with the standard topology.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": True,
                "connected": True, "path_connected": True, "simply_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.real_n_space,  # type: ignore[arg-type]
            aliases=["Euclidean n-space", "R^n"],
        ),
        SpaceRecord(
            name="Sorgenfrey plane",
            description="S_l x S_l; product of two Sorgenfrey lines. Separable Hausdorff but not normal.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": False,
                "compact": False, "locally_compact": False,
                "first_countable": True, "second_countable": False, "separable": True,
                "lindelof": False, "metrizable": False,
            },
            constructor=ns.sorgenfrey_plane,
            aliases=["S_l x S_l"],
        ),
        SpaceRecord(
            name="One-point compactification of N",
            description="Convergent sequence space {1/n : n>=1} union {0}; homeomorphic to omega+1.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": False, "path_connected": False,
                "totally_disconnected": True, "zero_dimensional": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.one_point_compactification_of_N,
            aliases=["convergent sequence space", "{0} union {1/n}"],
        ),
        SpaceRecord(
            name="omega+1",
            description="Successor ordinal {0,1,...,omega} with the order topology.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": False, "path_connected": False,
                "totally_disconnected": True, "zero_dimensional": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.omega_plus_1,
            aliases=["omega+1", "[0,omega]"],
        ),
        SpaceRecord(
            name="Rational sequence topology",
            description="R with rational-sequence neighborhoods at irrationals; T2 but not T3.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": False, "normal": False,
                "compact": False,
                "first_countable": True, "second_countable": False, "separable": True,
                "metrizable": False,
            },
            constructor=ns.rational_sequence_topology,
            aliases=["RST", "rational sequence space"],
        ),
        SpaceRecord(
            name="Particular point topology on R",
            description="Topology on R where U is open iff 0 in U (or U=empty); uncountable PPT.",
            properties={
                "t0": True, "t1": False, "hausdorff": False,
                "compact": False,
                "connected": True, "hyperconnected": True,
                "first_countable": True, "second_countable": False, "separable": True,
            },
            constructor=ns.particular_point_topology_on_R,
            aliases=["uncountable PPT", "PPT on R"],
        ),
        SpaceRecord(
            name="Excluded point topology on R",
            description="Topology on R where U is open iff 0 not in U or U=R; uncountable EPT.",
            properties={
                "t0": True, "t1": False, "hausdorff": False,
                "compact": False,
                "connected": True,
                "first_countable": True, "second_countable": False, "separable": False,
            },
            constructor=ns.excluded_point_topology_on_R,
            aliases=["uncountable EPT", "EPT on R"],
        ),
        SpaceRecord(
            name="Divisor topology",
            description="Topology on N+ where open sets are downward-closed under divisibility.",
            properties={
                "t0": True, "t1": False, "hausdorff": False,
                "compact": False,
                "connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
            },
            constructor=ns.divisor_topology,
            aliases=["divisibility topology", "arithmetic topology on N+"],
        ),
        SpaceRecord(
            name="Uncountable discrete space",
            description="R with the discrete topology; metrizable, locally compact, not separable.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": True,
                "connected": False, "totally_disconnected": True, "zero_dimensional": True,
                "first_countable": True, "second_countable": False, "separable": False,
                "lindelof": False, "metrizable": True,
            },
            constructor=ns.uncountable_discrete_space,
            aliases=["R discrete", "discrete uncountable space"],
        ),
        SpaceRecord(
            name="Double arrow space",
            description="[0,1] x {0,1} with lex order topology; homeomorphic to the Cantor set.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": False, "path_connected": False,
                "totally_disconnected": True, "zero_dimensional": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.double_arrow_space,
            aliases=["split interval", "two arrows"],
        ),
        SpaceRecord(
            name="Annulus",
            description="Closed annulus {(x,y) in R^2 : 1/4 <= x^2+y^2 <= 1}; retracts to S^1.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": True, "path_connected": True, "simply_connected": False,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.annulus,
            aliases=["closed annulus", "A"],
        ),
        SpaceRecord(
            name="Wedge of 2 circles",
            description="Wedge sum S^1 v S^1; fundamental group is free group on 2 generators.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": True, "path_connected": True, "simply_connected": False,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.wedge_sum_of_circles,
            aliases=["S^1 v S^1", "figure eight"],
        ),
        # ── Batch 7 ──────────────────────────────────────────────────────────
        SpaceRecord(
            name="Upper half-plane",
            description="H = {(x,y) in R^2 : y > 0}; open 2-manifold homeomorphic to R^2.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": True,
                "connected": True, "path_connected": True, "simply_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.upper_half_plane,
            aliases=["H", "Poincare half-plane"],
        ),
        SpaceRecord(
            name="Closed upper half-plane",
            description="H_closed = {(x,y) in R^2 : y >= 0}; 2-manifold with boundary, contractible.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": True,
                "connected": True, "path_connected": True, "simply_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.closed_upper_half_plane,
            aliases=["H_bar", "closed half-plane"],
        ),
        SpaceRecord(
            name="p-adic numbers",
            description="p-adic field Q_p with the p-adic metric; locally compact, totally disconnected.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": True,
                "connected": False, "path_connected": False,
                "totally_disconnected": True, "zero_dimensional": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.p_adic_numbers,
            aliases=["Q_p", "p-adic field"],
        ),
        SpaceRecord(
            name="Sierpinski triangle",
            description="Self-similar fractal gasket in R^2; compact, path-connected, not simply connected.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": True, "path_connected": True, "simply_connected": False,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.sierpinski_triangle,
            aliases=["Sierpinski gasket", "Sierpinski carpet (1D)"],
        ),
        SpaceRecord(
            name="RP^n",
            description="Real projective n-space RP^n = S^n / antipodal map; compact n-manifold.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": True, "path_connected": True, "simply_connected": False,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.real_projective_n_space,  # type: ignore[arg-type]
            aliases=["real projective n-space"],
        ),
        SpaceRecord(
            name="Cofinite topology on Z",
            description="Integers with cofinite topology; T1, compact, hyperconnected, not Hausdorff.",
            properties={
                "t0": True, "t1": True, "hausdorff": False,
                "compact": True,
                "connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": False,
            },
            constructor=ns.cofinite_topology_on_integers,
            aliases=["finite complement topology on Z"],
        ),
        SpaceRecord(
            name="Long ray",
            description="[0,omega_1) x [0,1) with lex order topology; connected 1-manifold, not separable.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": True,
                "connected": True, "path_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": False, "separable": False,
                "lindelof": False, "metrizable": False,
            },
            constructor=ns.long_ray,
            aliases=["L", "positive long ray"],
        ),
        SpaceRecord(
            name="Knaster continuum",
            description="Bucket-handle arc-like continuum over the Cantor set; compact, not locally connected.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": True, "path_connected": False,
                "locally_connected": False, "locally_path_connected": False,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.knaster_continuum,
            aliases=["bucket handle", "Knaster bucket handle"],
        ),
        SpaceRecord(
            name="Complex projective plane",
            description="CP^2 = (C^3 \\ {0}) / scalar; compact 4-manifold, simply connected.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": True, "path_connected": True, "simply_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.complex_projective_plane,
            aliases=["CP^2"],
        ),
        SpaceRecord(
            name="Infinite product of reals",
            description="R^omega = countable product of R with product topology; metrizable, not locally compact.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": False,
                "connected": True, "path_connected": True, "simply_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.infinite_product_of_reals,
            aliases=["R^omega", "R^N"],
        ),
        SpaceRecord(
            name="T^n",
            description="n-torus T^n = (S^1)^n; compact n-manifold with pi_1 = Z^n.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": True, "locally_compact": True,
                "connected": True, "path_connected": True, "simply_connected": False,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "metrizable": True,
            },
            constructor=ns.n_torus,  # type: ignore[arg-type]
            aliases=["n-torus"],
        ),
        SpaceRecord(
            name="Open unit disk",
            description="B^2 = {(x,y) in R^2 : x^2+y^2 < 1}; homeomorphic to R^2.",
            properties={
                "t0": True, "t1": True, "hausdorff": True,
                "regular": True, "normal": True,
                "compact": False, "locally_compact": True,
                "connected": True, "path_connected": True, "simply_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "lindelof": True, "metrizable": True,
            },
            constructor=ns.open_unit_disk,
            aliases=["B^2", "open disk"],
        ),
        # ── Batch 8 ──────────────────────────────────────────────────────────
        SpaceRecord(
            name="Genus-g surface",
            description="Closed orientable surface Sigma_g of genus g; compact, connected.",
            properties={
                "compact": True, "connected": True, "path_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "locally_compact": True, "metrizable": True, "hausdorff": True,
                "normal": True, "second_countable": True, "first_countable": True,
                "separable": True,
            },
            constructor=ns.genus_g_surface,
            aliases=["genus g surface", "Sigma_g"],
        ),
        SpaceRecord(
            name="n-ball",
            description="Closed n-ball D^n; compact, contractible, simply connected.",
            properties={
                "compact": True, "connected": True, "path_connected": True,
                "simply_connected": True, "contractible": True,
                "locally_connected": True, "locally_path_connected": True,
                "locally_compact": True, "metrizable": True, "hausdorff": True,
                "normal": True, "second_countable": True, "first_countable": True,
                "separable": True, "lindelof": True,
            },
            constructor=ns.n_ball,
            aliases=["D^n", "closed n-ball"],
        ),
        SpaceRecord(
            name="K-topology on R",
            description="R with K-topology: (a,b) and (a,b)\\K as basis; T2 but not T3.",
            properties={
                "connected": True, "hausdorff": True, "t1": True, "t0": True,
                "first_countable": True, "second_countable": True,
                "separable": True, "lindelof": True,
                "not_regular": True, "not_compact": True, "not_metrizable": True,
            },
            constructor=ns.k_topology_on_R,
            aliases=["K-topology", "R_K"],
        ),
        SpaceRecord(
            name="Dyadic solenoid",
            description="Inverse limit of S^1 under doubling maps; compact, not locally connected.",
            properties={
                "compact": True, "connected": True, "metrizable": True,
                "hausdorff": True, "normal": True,
                "first_countable": True, "second_countable": True, "separable": True,
                "not_path_connected": True, "not_locally_connected": True,
            },
            constructor=ns.solenoid,
            aliases=["solenoid"],
        ),
        SpaceRecord(
            name="Extended real line",
            description="[-inf,+inf] with order topology; homeomorphic to [0,1].",
            properties={
                "compact": True, "connected": True, "path_connected": True,
                "simply_connected": True, "contractible": True,
                "locally_connected": True, "locally_path_connected": True,
                "locally_compact": True, "metrizable": True, "hausdorff": True,
                "normal": True, "second_countable": True, "first_countable": True,
                "separable": True, "lindelof": True,
            },
            constructor=ns.extended_real_line,
            aliases=["[-inf,+inf]", "extended reals"],
        ),
        SpaceRecord(
            name="{0,1}^c",
            description="{0,1}^c: uncountable product; compact, Hausdorff, separable, not metrizable.",
            properties={
                "compact": True, "hausdorff": True, "t1": True, "t0": True,
                "normal": True, "separable": True,
                "zero_dimensional": True, "totally_disconnected": True,
                "not_connected": True, "not_metrizable": True,
                "not_first_countable": True, "not_second_countable": True,
            },
            constructor=ns.uncountable_product_of_two_point_spaces,
            aliases=["uncountable product of two-point spaces", "{0,1}^R"],
        ),
        SpaceRecord(
            name="S^2 v S^2",
            description="Wedge of two 2-spheres; simply connected, compact, not contractible.",
            properties={
                "compact": True, "connected": True, "path_connected": True,
                "simply_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "locally_compact": True, "metrizable": True, "hausdorff": True,
                "normal": True, "second_countable": True, "first_countable": True,
                "separable": True,
                "not_contractible": True,
            },
            constructor=ns.wedge_of_two_spheres,
            aliases=["wedge of two spheres", "S2 v S2"],
        ),
        SpaceRecord(
            name="Suspension of Cantor set",
            description="SC: suspension of the Cantor set; compact, path-connected, not locally connected.",
            properties={
                "compact": True, "connected": True, "path_connected": True,
                "metrizable": True, "hausdorff": True, "normal": True,
                "second_countable": True, "first_countable": True, "separable": True,
                "not_locally_connected": True,
            },
            constructor=ns.suspension_of_cantor_set,
            aliases=["SC"],
        ),
        SpaceRecord(
            name="Quarter plane",
            description="[0,inf)x[0,inf): contractible, simply connected, locally compact.",
            properties={
                "connected": True, "path_connected": True,
                "simply_connected": True, "contractible": True,
                "locally_connected": True, "locally_path_connected": True,
                "locally_compact": True, "metrizable": True, "hausdorff": True,
                "normal": True, "second_countable": True, "first_countable": True,
                "separable": True, "lindelof": True,
                "not_compact": True,
            },
            constructor=ns.quarter_plane,
            aliases=["[0,inf)^2", "closed quarter-plane"],
        ),
        SpaceRecord(
            name="Punctured torus",
            description="T^2 minus a point; homotopy equiv to S^1 v S^1, pi_1 = F_2.",
            properties={
                "connected": True, "path_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "locally_compact": True, "metrizable": True, "hausdorff": True,
                "normal": True, "second_countable": True, "first_countable": True,
                "separable": True, "lindelof": True,
                "not_compact": True, "not_simply_connected": True,
            },
            constructor=ns.punctured_torus,
            aliases=["T^2 \\ pt"],
        ),
        SpaceRecord(
            name="Countable disjoint union of circles",
            description="Disjoint union of countably many S^1; locally compact, sigma-compact.",
            properties={
                "locally_compact": True, "locally_connected": True,
                "locally_path_connected": True, "metrizable": True,
                "hausdorff": True, "normal": True,
                "second_countable": True, "first_countable": True, "separable": True,
                "sigma_compact": True,
                "not_compact": True, "not_connected": True,
            },
            constructor=ns.discrete_sum_of_circles,
            aliases=["coprod S^1"],
        ),
        SpaceRecord(
            name="Lens space",
            description="L(p,q): compact 3-manifold with pi_1 = Z/pZ.",
            properties={
                "compact": True, "connected": True, "path_connected": True,
                "locally_connected": True, "locally_path_connected": True,
                "locally_compact": True, "metrizable": True, "hausdorff": True,
                "normal": True, "second_countable": True, "first_countable": True,
                "separable": True,
            },
            constructor=ns.lens_space,
            aliases=["L(p,q)"],
        ),
    ]
    return SpaceCatalog(records)


catalog: SpaceCatalog = _build_default_catalog()

__all__ = [
    "SpaceRecord",
    "SpaceCatalog",
    "catalog",
]
