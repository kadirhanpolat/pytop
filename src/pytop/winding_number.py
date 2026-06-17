"""Winding numbers, circle-map degree, and planar vector-field index.

These are the constructive companions to the descriptive ``degree_theory``
profiles: each computes an integer topological invariant from sampled geometric
data, dependency-free.

* ``winding_number`` -- how many times a closed planar polyline wraps around a
  point, by accumulating signed subtended angles;
* ``circle_map_degree`` -- the degree of a map ``S^1 -> S^1`` from the ordered
  images of sample points (the winding number of the image path);
* ``vector_field_index`` -- the index of an isolated zero of a planar vector
  field, from the field values sampled around a small loop.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

Point = tuple[float, float]


class WindingError(ValueError):
    """Raised when winding data is degenerate (e.g. a sample hits the center)."""


def _signed_angle(ax: float, ay: float, bx: float, by: float) -> float:
    """Return the signed angle in (-pi, pi] from vector a to vector b."""

    if (ax == 0.0 and ay == 0.0) or (bx == 0.0 and by == 0.0):
        raise WindingError("A sampled vector has zero length (passes through the center).")
    cross = ax * by - ay * bx
    dot = ax * bx + ay * by
    return math.atan2(cross, dot)


def _total_turning(vectors: Sequence[Point]) -> int:
    """Accumulate signed angle change around a closed sequence of vectors."""

    if len(vectors) < 3:
        raise WindingError("At least three samples are required to determine winding.")
    total = 0.0
    count = len(vectors)
    for i in range(count):
        ax, ay = vectors[i]
        bx, by = vectors[(i + 1) % count]
        total += _signed_angle(ax, ay, bx, by)
    return round(total / (2.0 * math.pi))


def winding_number(loop: Sequence[Point], center: Point = (0.0, 0.0)) -> int:
    """Return the winding number of a closed polyline ``loop`` around ``center``.

    ``loop`` is an ordered sequence of points; the last point is joined back to
    the first. The result is positive for counterclockwise enclosure.
    """

    cx, cy = center
    vectors = [(x - cx, y - cy) for x, y in loop]
    return _total_turning(vectors)


def circle_map_degree(image_points: Sequence[Point]) -> int:
    """Return the degree of a map ``S^1 -> S^1`` from the ordered image samples.

    ``image_points`` are the images (points of the plane, nonzero) of evenly
    spaced domain samples traversed once around the circle. The degree is the
    winding number of the image path around the origin.
    """

    return _total_turning(list(image_points))


def vector_field_index(field_values: Sequence[Point]) -> int:
    """Return the index of an isolated zero of a planar vector field.

    ``field_values`` are the vectors ``(vx, vy)`` sampled counterclockwise along
    a small loop enclosing the zero. The index is the winding number of the
    field around the origin of vector space.
    """

    return _total_turning(list(field_values))


__all__ = [
    "WindingError",
    "winding_number",
    "circle_map_degree",
    "vector_field_index",
]
