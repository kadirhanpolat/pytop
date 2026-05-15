"""Polygon edge-identification helpers for the geometric topology bridge.

The module adds the GEO-07 surface-gluing layer. It parses small teaching edge
words such as ``a b a^-1 b^-1`` and records standard polygon models. It validates
finite edge-pairing syntax and gives a convention-bound orientability heuristic,
but it does not classify arbitrary quotient spaces.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence
from .surfaces import SurfaceProfile, known_surface_profile, surface_profile_summary

class SurfaceGluingError(ValueError):
    """Raised when a polygon gluing word or profile is malformed."""

GLUING_PROFILE_STATUSES = frozenset({"certified", "heuristic", "preview", "unknown"})
ORIENTABILITY_HEURISTIC_VALUES = frozenset({"orientable", "nonorientable", "unknown"})

@dataclass(frozen=True)
class EdgeToken:
    """One oriented occurrence of a boundary edge label in a polygon word."""
    label: str
    orientation: int = 1
    def __post_init__(self) -> None:
        label = str(self.label).strip(); orient = int(self.orientation)
        if not label: raise SurfaceGluingError("An edge token needs a nonempty label.")
        if orient not in {-1, 1}: raise SurfaceGluingError("Edge-token orientation must be +1 or -1.")
        object.__setattr__(self, "label", label); object.__setattr__(self, "orientation", orient)
    @property
    def inverse(self) -> "EdgeToken": return EdgeToken(self.label, -self.orientation)
    def normalized_text(self) -> str: return self.label if self.orientation == 1 else f"{self.label}^-1"

@dataclass(frozen=True)
class EdgePairingDiagnostic:
    """Diagnostic information for labels in an edge-identification word."""
    is_valid: bool
    paired_labels: tuple[str, ...]
    boundary_labels: tuple[str, ...] = ()
    overused_labels: tuple[str, ...] = ()
    label_counts: dict[str, int] = field(default_factory=dict, compare=False)
    warnings: tuple[str, ...] = ()
    @property
    def has_boundary_edges(self) -> bool: return bool(self.boundary_labels)

@dataclass(frozen=True)
class PolygonGluingProfile:
    """A conservative profile for a single polygon edge-identification model."""
    name: str
    edge_word: tuple[str, ...]
    expected_surface_key: str = ""
    allow_boundary_edges: bool = False
    convention: str = "counterclockwise boundary word; x^-1 denotes reversed orientation"
    status: str = "preview"
    warnings: tuple[str, ...] = ()
    related_profiles: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)
    def __post_init__(self) -> None:
        name = str(self.name).strip(); status = str(self.status)
        if not name: raise SurfaceGluingError("A gluing profile needs a nonempty name.")
        if status not in GLUING_PROFILE_STATUSES: raise SurfaceGluingError(f"Unsupported gluing profile status: {self.status!r}.")
        tokens = tuple(token.normalized_text() for token in parse_edge_word(self.edge_word))
        object.__setattr__(self, "name", name); object.__setattr__(self, "edge_word", tokens); object.__setattr__(self, "expected_surface_key", str(self.expected_surface_key))
        object.__setattr__(self, "allow_boundary_edges", bool(self.allow_boundary_edges)); object.__setattr__(self, "convention", str(self.convention)); object.__setattr__(self, "status", status)
        object.__setattr__(self, "warnings", tuple(str(w) for w in self.warnings)); object.__setattr__(self, "related_profiles", tuple(str(p) for p in self.related_profiles)); object.__setattr__(self, "metadata", dict(self.metadata))
    @property
    def tokens(self) -> tuple[EdgeToken, ...]: return parse_edge_word(self.edge_word)
    @property
    def labels(self) -> tuple[str, ...]: return tuple(t.label for t in self.tokens)
    @property
    def pairing_diagnostic(self) -> EdgePairingDiagnostic: return validate_edge_pairing(self.edge_word, allow_boundary_edges=self.allow_boundary_edges)
    @property
    def orientability_hint(self) -> str: return orientability_heuristic(self.edge_word, allow_boundary_edges=self.allow_boundary_edges)

def parse_edge_token(token: str | EdgeToken) -> EdgeToken:
    if isinstance(token, EdgeToken): return token
    text = str(token).strip()
    if not text: raise SurfaceGluingError("Empty edge token in gluing word.")
    if text.startswith("-") and len(text) > 1: return EdgeToken(text[1:].strip(), -1)
    for suffix in ("^-1", "^{-1}", "-1"):
        if text.endswith(suffix): return EdgeToken(text[:-len(suffix)].strip(), -1)
    return EdgeToken(text, 1)
def parse_edge_word(edge_word: str | Sequence[str | EdgeToken]) -> tuple[EdgeToken, ...]:
    raw = tuple(edge_word.split()) if isinstance(edge_word, str) else tuple(edge_word)
    if not raw: raise SurfaceGluingError("A polygon gluing word needs at least one edge token.")
    return tuple(parse_edge_token(t) for t in raw)
def normalized_edge_word(edge_word: str | Sequence[str | EdgeToken]) -> tuple[str, ...]: return tuple(t.normalized_text() for t in parse_edge_word(edge_word))
def edge_label_counts(edge_word: str | Sequence[str | EdgeToken]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for t in parse_edge_word(edge_word): counts[t.label] = counts.get(t.label, 0) + 1
    return counts
def validate_edge_pairing(edge_word: str | Sequence[str | EdgeToken], *, allow_boundary_edges: bool=False) -> EdgePairingDiagnostic:
    counts = edge_label_counts(edge_word)
    paired = tuple(sorted(k for k,v in counts.items() if v == 2)); boundary = tuple(sorted(k for k,v in counts.items() if v == 1)); overused = tuple(sorted(k for k,v in counts.items() if v > 2))
    warnings=[]
    if boundary and not allow_boundary_edges: warnings.append("Some labels occur once; treat them as boundary edges only when allow_boundary_edges=True.")
    if overused: warnings.append("Some labels occur more than twice; this helper does not model multi-pair identifications.")
    return EdgePairingDiagnostic(not overused and (allow_boundary_edges or not boundary), paired, boundary, overused, counts, tuple(warnings))
def label_orientation_pattern(edge_word: str | Sequence[str | EdgeToken]) -> dict[str, tuple[int, ...]]:
    d: dict[str, list[int]] = {}
    for t in parse_edge_word(edge_word): d.setdefault(t.label, []).append(t.orientation)
    return {k: tuple(v) for k,v in d.items()}
def orientability_heuristic(edge_word: str | Sequence[str | EdgeToken], *, allow_boundary_edges: bool=False) -> str:
    diag = validate_edge_pairing(edge_word, allow_boundary_edges=allow_boundary_edges)
    if not diag.is_valid: return "unknown"
    pairs = [v for v in label_orientation_pattern(edge_word).values() if len(v) == 2]
    if not pairs: return "unknown"
    if any(v[0] == v[1] for v in pairs): return "nonorientable"
    if all(sorted(v) == [-1, 1] for v in pairs): return "orientable"
    return "unknown"
def polygon_gluing_profile(name: str, edge_word: str | Sequence[str | EdgeToken], *, expected_surface_key: str="", allow_boundary_edges: bool=False, convention: str="counterclockwise boundary word; x^-1 denotes reversed orientation", status: str="preview", warnings: Iterable[str]=(), related_profiles: Iterable[str]=(), metadata: dict[str, Any]|None=None) -> PolygonGluingProfile:
    return PolygonGluingProfile(name, normalized_edge_word(edge_word), expected_surface_key, allow_boundary_edges, convention, status, tuple(warnings), tuple(related_profiles), dict(metadata or {}))
def sphere_gluing_profile() -> PolygonGluingProfile: return polygon_gluing_profile("sphere_edge_pairing", "a a^-1", expected_surface_key="sphere", status="certified", warnings=("This is a standard two-gon model; no classification proof is supplied.",), related_profiles=("surfaces","quotients"))
def torus_gluing_profile() -> PolygonGluingProfile: return polygon_gluing_profile("torus_square_gluing", "a b a^-1 b^-1", expected_surface_key="torus", status="certified", warnings=("The word is a standard torus model under the stated boundary convention.",), related_profiles=("surfaces","fundamental_group","quotients"))
def projective_plane_gluing_profile() -> PolygonGluingProfile: return polygon_gluing_profile("projective_plane_gluing", "a a", expected_surface_key="projective_plane", status="certified", warnings=("The same-orientation pair records the standard projective-plane model.",), related_profiles=("surfaces","projective_spaces","quotients"))
def klein_bottle_gluing_profile() -> PolygonGluingProfile: return polygon_gluing_profile("klein_bottle_square_gluing", "a b a^-1 b", expected_surface_key="klein_bottle", status="certified", warnings=("This profile records the standard Klein-bottle word only.",), related_profiles=("surfaces","quotients"))
def mobius_band_gluing_profile() -> PolygonGluingProfile: return polygon_gluing_profile("mobius_band_rectangle_gluing", "a b a b^-1", expected_surface_key="mobius_band", status="heuristic", warnings=("This rectangle word is a teaching model, not a classifier.",), related_profiles=("surfaces","quotients"), metadata={"has_boundary": True})
STANDARD_GLUING_PROFILES: Mapping[str, PolygonGluingProfile] = {"sphere":sphere_gluing_profile(),"sphere_s2":sphere_gluing_profile(),"s2":sphere_gluing_profile(),"torus":torus_gluing_profile(),"torus_t2":torus_gluing_profile(),"t2":torus_gluing_profile(),"projective_plane":projective_plane_gluing_profile(),"projective_plane_rp2":projective_plane_gluing_profile(),"rp2":projective_plane_gluing_profile(),"klein_bottle":klein_bottle_gluing_profile(),"mobius_band":mobius_band_gluing_profile(),"moebius_band":mobius_band_gluing_profile()}
def standard_gluing_profile(key: str) -> PolygonGluingProfile:
    norm = str(key).strip().lower().replace(" ", "_").replace("-", "_").replace("^", "")
    return STANDARD_GLUING_PROFILES.get(norm) or polygon_gluing_profile(f"{norm or 'unknown'}_unknown_gluing", "u u^-1", status="unknown", warnings=("No registered standard gluing profile for this key; placeholder word is not a recognition result.",))
def compare_gluing_to_surface_profile(profile: PolygonGluingProfile, surface: SurfaceProfile | str | None=None) -> dict[str, Any]:
    if isinstance(surface, SurfaceProfile):
        sp = surface
    else:
        sp = known_surface_profile(surface or profile.expected_surface_key or profile.name)
    hint = profile.orientability_hint
    return {"gluing_name": profile.name, "edge_word": profile.edge_word, "pairing_valid": profile.pairing_diagnostic.is_valid, "orientability_hint": hint, "surface_name": sp.name, "surface_orientability": sp.orientability, "surface_status": sp.status, "orientability_matches": hint != "unknown" and hint == sp.orientability, "surface_summary": surface_profile_summary(sp), "warnings": profile.warnings + profile.pairing_diagnostic.warnings + sp.warnings}
def gluing_profile_summary(profile: PolygonGluingProfile) -> dict[str, Any]:
    d = profile.pairing_diagnostic
    return {"name": profile.name, "edge_word": profile.edge_word, "expected_surface_key": profile.expected_surface_key, "pairing_valid": d.is_valid, "paired_labels": d.paired_labels, "boundary_labels": d.boundary_labels, "overused_labels": d.overused_labels, "label_counts": d.label_counts, "orientability_hint": profile.orientability_hint, "status": profile.status, "convention": profile.convention, "warnings": profile.warnings + d.warnings}
__all__ = [name for name in globals() if not name.startswith("_")]
