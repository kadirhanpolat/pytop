"""Known-answer tests for closed-surface classification from gluing words."""

from __future__ import annotations

import pytest

from pytop import classify_surface_word
from pytop.surface_gluing import SurfaceGluingError


def test_sphere():
    s = classify_surface_word("a a^-1")
    assert s.euler_characteristic == 2
    assert s.orientable is True
    assert s.genus == 0
    assert s.name == "sphere"


def test_torus():
    s = classify_surface_word("a b a^-1 b^-1")
    assert s.euler_characteristic == 0
    assert s.orientable is True
    assert s.genus == 1
    assert s.name == "torus"


def test_projective_plane():
    s = classify_surface_word("a a")
    assert s.euler_characteristic == 1
    assert s.orientable is False
    assert s.genus == 1
    assert s.name == "projective plane"


def test_klein_bottle():
    s = classify_surface_word("a b a^-1 b")
    assert s.euler_characteristic == 0
    assert s.orientable is False
    assert s.genus == 2
    assert s.name == "Klein bottle"


def test_genus_two_orientable():
    # standard octagon word for the genus-2 orientable surface
    s = classify_surface_word("a b a^-1 b^-1 c d c^-1 d^-1")
    assert s.euler_characteristic == -2
    assert s.orientable is True
    assert s.genus == 2
    assert s.name == "orientable genus-2 surface"


def test_connected_sum_two_projective_planes_is_klein():
    # RP^2 # RP^2 = Klein bottle, word "a a b b": non-orientable, chi = 0
    s = classify_surface_word("a a b b")
    assert s.euler_characteristic == 0
    assert s.orientable is False
    assert s.genus == 2
    assert s.name == "Klein bottle"


def test_boundary_word_detected():
    # 'c' occurs once -> boundary edge; not a closed surface
    s = classify_surface_word("a b a^-1 c")
    assert s.has_boundary is True
    assert s.genus is None


def test_overused_label_raises():
    with pytest.raises(SurfaceGluingError):
        classify_surface_word("a a a")
