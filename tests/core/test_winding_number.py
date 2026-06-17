"""Known-answer tests for winding number, circle-map degree, and field index."""

from __future__ import annotations

import math

import pytest

from pytop import circle_map_degree, vector_field_index, winding_number
from pytop.winding_number import WindingError


def _circle_samples(n, turns=1, radius=1.0):
    return [
        (radius * math.cos(2 * math.pi * turns * k / n), radius * math.sin(2 * math.pi * turns * k / n))
        for k in range(n)
    ]


# --------------------------------------------------------------------------
# winding_number
# --------------------------------------------------------------------------

def test_ccw_loop_winds_once():
    assert winding_number(_circle_samples(12)) == 1


def test_cw_loop_winds_negative():
    assert winding_number(_circle_samples(12, turns=-1)) == -1


def test_double_loop_winds_twice():
    assert winding_number(_circle_samples(24, turns=2)) == 2


def test_loop_not_enclosing_center_is_zero():
    # a small square far from the origin
    square = [(10.0, 0.0), (11.0, 0.0), (11.0, 1.0), (10.0, 1.0)]
    assert winding_number(square) == 0


def test_winding_around_offset_center():
    loop = [(x + 5, y + 5) for x, y in _circle_samples(12)]
    assert winding_number(loop, center=(5.0, 5.0)) == 1


def test_sample_through_center_raises():
    with pytest.raises(WindingError):
        winding_number([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])


# --------------------------------------------------------------------------
# circle_map_degree
# --------------------------------------------------------------------------

def test_identity_map_degree_one():
    assert circle_map_degree(_circle_samples(16)) == 1


def test_squaring_map_degree_two():
    # z -> z^2 doubles the angle
    n = 24
    images = [(math.cos(2 * 2 * math.pi * k / n), math.sin(2 * 2 * math.pi * k / n)) for k in range(n)]
    assert circle_map_degree(images) == 2


def test_constant_map_winds_zero():
    images = [(1.0, 0.0)] * 12
    assert circle_map_degree(images) == 0


# --------------------------------------------------------------------------
# vector_field_index
# --------------------------------------------------------------------------

def test_radial_field_index_one():
    # v(p) = p  -> source, index +1
    loop = _circle_samples(16)
    assert vector_field_index(loop) == 1


def test_saddle_field_index_negative_one():
    # v(x, y) = (x, -y) -> saddle, index -1
    loop = _circle_samples(24)
    field = [(x, -y) for x, y in loop]
    assert vector_field_index(field) == -1
