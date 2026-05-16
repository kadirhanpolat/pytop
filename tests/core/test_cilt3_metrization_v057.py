"""Tests for v0.1.57 Cilt III metrization directions corridor.

Covers metrization_profiles.py v0.1.57 additions:
  - is_metrizable: finite discrete exact, finite non-discrete false,
    negative tags, positive tags, Urysohn criterion, unknown
  - metrization_profile: profile dict shape
  - analyze_metrization: single-call facade
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import importlib.util


# Load metrization_profiles from source to bypass stale .pyc
def _load_fresh(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    mod.__package__ = 'pytop'
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

BASE = os.path.join(os.path.dirname(__file__), '../../src')
_mp = _load_fresh('pytop.metrization_api',
    os.path.join(BASE, 'pytop/metrization_api.py'))

from pytop.finite_spaces import FiniteTopologicalSpace  # noqa: E402

is_metrizable = _mp.is_metrizable
metrization_profile = _mp.metrization_profile
analyze_metrization = _mp.analyze_metrization
MetrizationError = _mp.MetrizationError

def _discrete2():
    return FiniteTopologicalSpace(
        carrier=['a', 'b'],
        topology=[frozenset(), frozenset(['a']), frozenset(['b']), frozenset(['a', 'b'])],
    )

def _sierpinski():
    return FiniteTopologicalSpace(
        carrier=[0, 1],
        topology=[frozenset(), frozenset([1]), frozenset([0, 1])],
    )

def _three_point_non_discrete():
    return FiniteTopologicalSpace(
        carrier=['a', 'b', 'c'],
        topology=[frozenset(), frozenset(['a']), frozenset(['a', 'b']), frozenset(['a', 'b', 'c'])],
    )

class _Tagged:
    def __init__(self, tags):
        self.tags = tags
        self.representation = "symbolic_general"

p = f = 0
def ck(n, c):
    global p, f
    if c: p += 1
    else: f += 1; print(f"  FAIL: {n}")

# --- finite discrete → true exact ---
r = is_metrizable(_discrete2())
ck("discrete2 true", r.status == "true")
ck("discrete2 exact", r.mode == "exact")
ck("discrete just discrete", "discrete" in " ".join(r.justification).lower())

# --- finite non-discrete → false ---
r = is_metrizable(_sierpinski())
ck("sierpinski false", r.status == "false")
r = is_metrizable(_three_point_non_discrete())
ck("three_point false", r.status == "false")
ck("non-discrete just not discrete", "discrete" in " ".join(r.justification).lower())

# --- negative tags → false ---
for tag in ("not_metrizable", "not_hausdorff", "not_first_countable"):
    r = is_metrizable(_Tagged([tag]))
    ck(f"neg tag {tag} false", r.status == "false")

# --- positive tags → true ---
for tag in ("metrizable", "metric", "second_countable_regular"):
    r = is_metrizable(_Tagged([tag]))
    ck(f"pos tag {tag} true", r.status == "true")
    ck(f"pos tag {tag} theorem", r.mode == "theorem")

# --- Urysohn criterion: second_countable + t3 → true ---
r = is_metrizable(_Tagged(["second_countable", "t3"]))
ck("urysohn criterion true", r.status == "true")
ck("urysohn criterion theorem", r.mode == "theorem")
ck("urysohn in justification", "urysohn" in " ".join(r.justification).lower())
ck("criterion metadata", r.metadata.get("criterion") == "urysohn_metrization")

# second_countable + regular also works
r = is_metrizable(_Tagged(["second_countable", "regular"]))
ck("urysohn 2nd_countable+regular true", r.status == "true")

# --- unknown ---
r = is_metrizable(_Tagged([]))
ck("no tags unknown", r.status == "unknown")
r = is_metrizable(_Tagged(["hausdorff"]))
ck("hausdorff alone unknown", r.status == "unknown")

# --- metrization_profile ---
pr = metrization_profile(_discrete2())
ck("profile has is_metrizable", "is_metrizable" in pr)
ck("profile has criterion", "criterion" in pr)
ck("profile has named_profiles", "named_profiles" in pr)
ck("profile discrete is_metrizable true", pr["is_metrizable"].status == "true")
ck("named_profiles non-empty", len(pr["named_profiles"]) > 0)

# --- analyze_metrization ---
r = analyze_metrization(_discrete2())
ck("analyze discrete true", r.status == "true")
for k in ("is_metrizable", "criterion", "named_profile_keys"):
    ck(f"analyze meta {k}", k in r.metadata)
ck("analyze meta is_metrizable=true", r.metadata["is_metrizable"] == "true")
ck("named_profile_keys non-empty", len(r.metadata["named_profile_keys"]) > 0)

# Urysohn via analyze
r = analyze_metrization(_Tagged(["second_countable", "t3"]))
ck("analyze urysohn true", r.status == "true")
ck("analyze urysohn criterion", r.metadata["criterion"] == "urysohn_metrization")

print(f"\n{'='*50}")
print(f"  {p} passed, {f} failed")
if f == 0:
    print("  ALL TESTS PASSED ✓")
