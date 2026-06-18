# CLAUDE.md

## Project

`pytop` is a standalone mathematical topology library for Python 3.11+.
It provides point-set topology, knot theory, graph topology, surface classification,
3-manifolds, degree theory, cardinal functions, and more. As of **v0.6.0+** it also ships a
**constructive computational core** (simplicial homology with field/relative coefficients,
persistent homology / TDA, optimized persistence with Twist+Clearing, cubical complexes +
bitmap persistence, knot invariant polynomials, winding/degree, surface-word classification,
exact graph planarity), a **pi-Base–backed deductive inference engine**
(`pytop.experimental.pi_base`), and a **research-grade computable-space protocol**
(`pytop.experimental.spaces`) for point-set topology — Phase 1 complete (S1–S5),
**Phase 2 complete (8/8)**: field-coeff homology, relative homology, Mayer–Vietoris LES,
cellular homology, cohomology + cup product, van Kampen → group presentations,
optimized persistence (Twist+Clearing), cubical complexes.

- **GitHub:** https://github.com/kadirhanpolat/pytop
- **License:** MIT
- **Version:** see `pyproject.toml` and `src/pytop/__init__.py` (`__version__`)

---

## Architecture: two layers

pytop has two complementary layers — keep this distinction in mind when extending it:

- **Descriptive** — `*Profile` dataclasses + `get_*_profiles()` registries that record curated,
  referenced facts about famous spaces/theorems (most algebraic/advanced modules). They *know*
  invariants; they do not compute them.
- **Constructive** — engines that *compute* invariants from raw input. The v0.6.0+ computational core:
  `homology` (integer boundary matrices → Smith normal form → Betti + torsion),
  `homology_coefficients` (field-coefficient / relative homology — Gaussian elimination over Q and Z/p),
  `mayer_vietoris` (Mayer–Vietoris LES: extended SNF with transformation matrices → explicit homology
  bases; φ, ψ, δ as integer matrices; exactness verified at every position; `_snf_ext` supports
  `compute_transforms=False` to skip P/Pinv/Q/Qinv updates when only D is needed — `_mat_rank`
  uses this path for ~80% inner-loop saving),
  `cellular_homology` (CW complex chain complex → SNF; standard spaces S^n, RP^n, CP^n, T², Klein
  bottle, lens spaces, Moore spaces; `cw_from_simplicial` cross-validation bridge),
  `cohomology` (cochain complex via δ^k=(∂_{k+1})^T; extended SNF → H^k; UCT verified;
  Alexander-Whitney cup product; `CohomologyRing` with graded-commutativity, torus pairing, and
  `verify_graded_commutativity()` method),
  `persistent_homology` (Vietoris–Rips filtration → Z/2 reduction → barcodes),
  `persistent_homology_optimized` (Twist algorithm, Chen–Kerber 2011: dimension-top-down sweep +
  Clearing Lemma; `ReductionStats` with n_cleared / clearing_ratio / n_column_additions;
  shared `_twist_reduce` kernel used by both simplicial and cubical pipelines; **bigint bitmask**
  column representation — `list[int]` Python bigint replaces `list[set[int]]`, pivot via
  `col.bit_length()-1`; ~6.6× kernel speedup),
  `cubical_homology` (`CubicalComplex` with face-closure + ℤ boundary matrix + SNF homology;
  `circle_cubical`, `disk_cubical`, `interval_complex`; `CubicalFiltration` +
  `bitmap_to_cubical_filtration` — lower-star filtration from 2-D pixel arrays with
  f(face) ≤ f(coface) guaranteed; `persistent_homology_bitmap` via Twist+Clearing),
  `van_kampen` (Seifert–van Kampen: GroupPresentation + GroupHomomorphism; amalgamated free
  product; Tietze elimination with cyclic reduction + inverse-duplicate deduplication;
  abelianization via SNF; group identification (`"free_abelian_rank_2"` for T²); CW1Complex route
  with disconnected 1-skeleton guard (raises ValueError); standard spaces S¹∨⋯∨S¹→Fₙ, S²→1,
  T²→ℤ², Klein→⟨a,b|abab⁻¹⟩, RP²→ℤ/2),
  `knot_invariants` (Kauffman→Jones, reduced Burau→Alexander), `winding_number`,
  `surface_word_classification`, `graph_planarity` (rotation-system genus), and
  `experimental.spaces` (research-grade computable-space protocol — see below).
  New computational work should prefer this constructive style.
- **Research-grade point-set layer** (`experimental.spaces`) — a third layer bridging the two above:
  a `Space` protocol + 16 witness-producing predicates + property-reasoning engine that derives
  and *explains* properties of constructed infinite spaces (preservation theorems + pi-Base
  implication graph). **10 representations**: `FiniteSpace`, `CofiniteSpace`, `OrderTopologySpace`,
  `MetricTopologySpace`, `SorgenfreyLineSpace`, `DiscreteCountableSpace`, `OpaqueInfiniteSpace`,
  `AlexandroffSpace` (upset topology of a preorder), `SubbaseSpace` (subbase-generated topology),
  `InverseLimitSpace` (finite inverse system + bonding maps). **Factory functions**:
  `finite_circle()` (4-pt diamond, π₁=ℤ), `finite_sphere(n)` (2(n+1)-pt suspension tower),
  `finite_wedge_circles(k)` (1+3k pt model of S¹∨⋯∨S¹, π₁=F_k). **Cardinal invariants**
  (`cardinal_invariants.py`): weight, density, character, cellularity — exact for finite spaces;
  `cardinal_certificate` hook on each infinite representation; `AlexandroffSpace.certificate`
  provides structural T0 (antisymmetry test) and connectedness (union-find on order graph) verdicts
  without open-set enumeration; `cardinal_certificate` returns character=1, weight=|X| (T0 case).
  **Urysohn witnesses** (`urysohn.py`): `UrysohnWitness` + `urysohn_function(space, x₀, C)`;
  discrete finite → exact indicator; general finite → BFS chain; `MetricTopologySpace` →
  distance-ratio formula; `SorgenfreyLineSpace` → Euclidean formula (τ_std ⊊ τ_Sorgenfrey);
  `OrderTopologySpace` → order-metric formula; `DiscreteCountableSpace` → discrete metric
  (d(x,y)=0 iff x=y) with `method="discrete_metric"` witness. **π₁ computation** (`pi1.py`): `pi1_space(space)`
  via McCord order complex (specialization order → CW1Complex → spanning-tree algorithm);
  T0 quotient for non-T0 inputs; `ProductSpace` → π₁(A)×π₁(B); `SumSpace` → π₁(first).
  **Tietze improvements** (`van_kampen.py`): `_cyclically_reduce` (prefix/suffix inverse-pair
  removal), `_dedup_relators` (duplicate relators up to cyclic conjugation + inversion),
  applied after every Tietze II elimination. `predicates._decide` checks `certificate` first
  so `AlexandroffSpace` (and future subclasses) give structural reasons without enumeration.
  `persistence_betti_numbers(pairs)` counts essential pairs per dimension.
  See `docs/CAPABILITIES_AND_ROADMAP.md` for Phase 1/2 status.

## pi-Base data

`pytop.experimental.pi_base` / `pi_base_atlas` load a compact JSON blob derived from the
[pi-Base](https://topology.pi-base.org) database (CC BY 4.0, Clontz & Dabbs): 243 properties,
902 implication theorems, 222 spaces, 2099 traits. Regenerate it from a local `pi-base/data`
checkout with:

```bash
py -3.14 -m pytop._internal.pi_base_compile --source <path-to-pi-base/data> \
    --out src/pytop/experimental/_pi_base_data.json
```

The compiler may use PyYAML (developer-only); the **runtime loads with stdlib `json`** (no new
dependency). Attribution lives in `PI_BASE_ATTRIBUTION`.

> **Copyright note:** `Topoloji/` holds copyrighted reference textbooks kept for local research
> only. It is git-ignored and must **never** be committed. Likewise, do not vendor the raw
> `pi-base/data` repository — only the derived, attributed JSON blob belongs in the package.

---

## Directory Structure

```
src/pytop/              ← public math API (import from here)
src/pytop/_internal/    ← internal tooling (chapter integration, audit tools, release scripts)
                          NOT exported in __init__.py, NOT part of public API
src/pytop/experimental/ ← research-stage modules (unstable API)
  spaces/               ← computable-space protocol (Phase 1 complete: Space, predicates,
                          reasoning engine, pi-Base bridge — see CAPABILITIES_AND_ROADMAP.md)
tests/core/             ← tests for src/pytop/
tests/experimental/     ← tests for src/pytop/experimental/
examples_bank/          ← topic-based Markdown example files (not importable)
docs/CAPABILITIES_AND_ROADMAP.md  ← honest capabilities assessment + phased roadmap
```

---

## Commands

```bash
# Install in editable mode
pip install -e .

# Run tests
pytest tests/ -q

# Run tests with coverage
pytest tests/ --cov=pytop --cov-report=term-missing

# Run only core tests
pytest tests/core/ -q

# Run only experimental tests
pytest tests/experimental/ -q
```

> **Python interpreter:** Always use `py -3.14` on this machine (not `python` or bare `py`).

---

## User Guide

Located at `docs/user_guide/`. Four parallel formats:

```
docs/user_guide/
  latex/              ← XeLaTeX source (main.tex, chapters/, appendix/, figures/)
  markdown/           ← Markdown files (one per chapter + solutions.md)
  python/             ← Percent-cell scripts (# %% / # %% [markdown])
  notebook/           ← Jupyter notebooks (.ipynb)
  assets/             ← Generated PNGs (ch04/, ch06/, ...)
  tools/              ← build_figures.py (TikZ→PNG pipeline)
```

**TikZ→PNG pipeline:** `py -3.14 docs/user_guide/tools/build_figures.py`
- Reads `.tikz` files from `latex/figures/`
- Compiles with `xelatex` (standalone.cls)
- Rasterizes at 300 dpi via `pdftoppm`
- Writes PNGs to `assets/chNN/`

**Maarif pedagogy blocks** (md + py + ipynb, all 16 chapters):
Every chapter has 5 blockquote blocks after `## 1. Konu`:
`> **Neden bu konu?**` / `> 🔍 **Kendin dene:**` / `> ⚠️ **Sık hata:**` /
`> ↗️ **Bkz.:**` / `> 💭 **Öz-yansıtma:**`
In Python files: `# %% [markdown]\n"""..."""` cell. In notebooks: markdown cell inserted after `## 1. Konu` cell.

**API style rule** (ch10 onwards): use `make_set(...)` / `empty_set()` instead of raw
`frozenset({...})` / `set()` in examples.

**Pedagogical tcolorbox environments** (defined in `latex/main.tex`):

| Environment | Color | Purpose |
|-------------|-------|---------|
| `sezgi` | blue | Intuition / motivating analogy |
| `dikkat` | orange | Common mistakes / warnings |
| `nedenonemli` | green | Why this matters |
| `karsiornek` | violet | Counter-examples |

**`\ipucu{...}` macro** — renders as italic hint text in exercise lists.

**Solutions appendix:** `latex/appendix/solutions.tex` + `markdown/solutions.md` + `python/solutions.py` + `notebook/solutions.ipynb`

**Compile PDF:**
```bash
cd docs/user_guide/latex && xelatex -interaction=nonstopmode main.tex
```

**Run a chapter script:**
```bash
py -3.14 docs/user_guide/python/ch04_topological_spaces.py
```

---

## Branching Strategy

```
master          ← stable releases, tagged (v0.4.0, v0.4.1, ...)
feature/<topic> ← feature branches, merge to master via PR
```

- Never commit directly to `master`
- Tag every release: `git tag vX.Y.Z && git push origin vX.Y.Z`
- **Latest release:** `feat/phase3-knot-suite` → `master` via PR #16, tagged **v0.8.0** — Phase 3 complete (P3.1 Seifert/LinkDiagram/HOMFLY-PT/multivariable Alexander, P3.2 `dehn_surgery`, P3.3 `khovanov`)
- **In progress:** Phase 4 — P4.1 property-based + cross-engine differential testing done (`tests/core/test_property_invariants.py`); 9 919 tests

---

## API Design Rules

1. **Public API lives in `src/pytop/__init__.py`** — every symbol intended for users must be explicitly exported there.

2. **`_internal/` is off-limits for users** — modules in `_internal/` must NOT appear in `__init__.py` exports. Prefix with `_` signals internal use.

3. **New experimental code goes to `src/pytop/experimental/` first** — once stable and tested, promote to core `src/pytop/` and re-export from `experimental/` for backward compatibility.

4. **No ecosystem dependencies** — `pytop_questionbank`, `pytop_pedagogy`, `pytop_publish` must NOT be imported anywhere in `src/pytop/` (not even inside try/except blocks in new code).

5. **`__version__` must be in sync** — `pyproject.toml` version and `src/pytop/__init__.py` `__version__` must always match.

---

## `pytop.experimental` Philosophy

`pytop.experimental` is the research buffer zone:
- Modules here may have unstable APIs
- Users import via `from pytop.experimental import ...`
- When a module is promoted to stable, keep it in `experimental/` as a re-export with a deprecation note
- Do not promote a module without tests

---

## Cilt / Corridor Terminology

Test files and `_internal/` modules use terminology from the original textbook
development context. This glossary decodes the key terms:

| Term | Meaning |
|------|---------|
| **Cilt** | Turkish for "volume". Cilt I–IV map to volumes of the source textbook. |
| **Cilt I** | Point-set topology foundations (sets, spaces, maps, compactness, connectedness, separation) |
| **Cilt II** | Metric spaces, completeness, counterexample atlas, preservation tables |
| **Cilt III** | Local compactness, metrization, neighborhood systems, function spaces, compactness variants |
| **Cilt IV** | Cardinal functions, cardinal numbers, ordinals, quantitative topology |
| **Corridor** | A development milestone version (e.g., `v0.1.47`) that added a specific feature set |
| **Route** | A sequence of corridors forming a complete coverage of a topic |
| **Close-out** | The final corridor that completes a cilt's coverage |
| **Route summary** | An `_internal` function that documents which corridors cover a given topic |
| **v0.X.YZ** | Internal milestone versions — not the same as the public package version (v0.4.0+) |

These terms appear in `_internal/` module names and test files (e.g.,
`test_cilt2_undergraduate_route_v050.py`). They are internal metadata only.

---

## Version Bump Checklist

1. Update `version` in `pyproject.toml`
2. Update `__version__` in `src/pytop/__init__.py`
3. Add entry to `CHANGELOG.md`
4. Commit: `git commit -m "chore: bump version to vX.Y.Z"`
5. Tag: `git tag vX.Y.Z`
6. Push: `git push origin master --tags`
