"""Generic, witness-producing predicates over the :class:`Space` protocol.

These algorithms target the protocol, not any concrete representation, and are
honest about decidability:

* **finite / enumerable** spaces are decided by computation (with a witness or a
  counterexample);
* **infinite** spaces are decided when the representation supplies a
  construction-level certificate (e.g. metric ⟹ Hausdorff);
* otherwise the verdict is reported as **undecidable** — never guessed.
"""

from __future__ import annotations

from itertools import combinations

from .core import Decidability, NotEnumerableError, Space, Verdict


def is_hausdorff(space: Space) -> Verdict:
    """Decide whether ``space`` is Hausdorff (T2), with a witness or counterexample.

    Finite spaces are decided by checking every pair of points for separating
    disjoint opens. Infinite spaces defer to ``separation_certificate("T2")``;
    without one the result is undecidable.
    """

    if space.is_finite():
        return _decide_finite_hausdorff(space)

    certificate = space.separation_certificate("T2")
    if certificate is not None:
        return certificate
    return Verdict.undecidable(
        f"{space.name!r}: infinite space without a Hausdorff certificate; "
        "cannot enumerate all point pairs."
    )


def _decide_finite_hausdorff(space: Space) -> Verdict:
    try:
        points = list(space.points())
    except NotEnumerableError:
        return Verdict.undecidable(f"{space.name!r}: carrier not enumerable.")

    checked = 0
    for x, y in combinations(points, 2):
        separation = space.point_separation(x, y)
        if separation.value is False:
            return Verdict.false(
                reason=f"{space.name!r}: {separation.reason}",
                counterexample=separation.counterexample or (x, y),
            )
        if separation.value is None:
            return Verdict(
                None,
                Decidability.UNDECIDABLE,
                reason=f"{space.name!r}: point separation undecidable for {(x, y)!r}",
            )
        checked += 1
    return Verdict.true(
        reason=f"{space.name!r}: all {checked} point pair(s) separated by disjoint opens",
        witness={"pairs_separated": checked},
    )


__all__ = ["is_hausdorff"]
