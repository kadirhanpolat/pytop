# Phase 20: Ecosystem & Release Maturity

**Status:** 🚧 In Progress  
**Date:** 2026-06-23  
**Scope:** PyPI publishing, CI/CD hardening, community onboarding

## Phase 20.1: CI/CD Hardening ✅

### Python Version Matrix

Updated GitHub Actions workflow to test on Python 3.11–3.14:

```yaml
python-version: ["3.11", "3.12", "3.13", "3.14"]
```

All tests pass on Python 3.14 (current development version).

### Build & Test Pipeline

✅ **Checks:**
- `ruff check src/pytop/` — linting
- `mypy src/pytop/` — type checking  
- `pytest tests/ --cov=pytop` — unit tests + coverage
- All checks **required before merge to master**

✅ **Coverage:**
- Current: >85% (11,685+ tests across 225 modules)
- Target: 85%+ maintained

✅ **Platforms:**
- Ubuntu (CI runner)
- Local Windows/macOS (developer machines)

### Version Support Policy

**Current support:**
- Python 3.11: Full support (released 2022)
- Python 3.12: Full support (released 2023)
- Python 3.13: Full support (released 2024)
- Python 3.14: Full support (released 2025, current development)

**End-of-life:** Support ends when Python version reaches EOL (typically ~3.5 years after release).

---

## Phase 20.2: PyPI Publishing (Planned)

### Pre-Release Checklist

- [ ] Version bumped in `pyproject.toml` and `src/pytop/__init__.py`
- [ ] `CHANGELOG.md` updated with release notes
- [ ] All CI checks passing on 4 Python versions
- [ ] Documentation build succeeds
- [ ] `build` and `twine` installed: `pip install build twine`

### Release Process

```bash
# 1. Bump version (e.g., v1.6.0 → v1.7.0)
# Update pyproject.toml and __init__.py

# 2. Build distribution
python -m build

# 3. Test locally (optional)
pip install --force-reinstall dist/pytop-1.7.0-py3-none-any.whl

# 4. Upload to TestPyPI (dry run)
twine upload --repository testpypi dist/*

# 5. Upload to PyPI (production)
twine upload dist/*

# 6. Tag release
git tag v1.7.0
git push origin v1.7.0
```

### PyPI Metadata

```python
[project]
name = "pytop"
version = "1.7.0"  # Bumped
description = "Mathematical topology library"
readme = "README.md"
requires-python = ">=3.11"
dependencies = []  # Zero runtime dependencies
```

✅ **Zero runtime dependencies** — pytop is self-contained.

---

## Phase 20.3: Community Onboarding (Planned)

### GitHub Issue Templates

Create `.github/ISSUE_TEMPLATE/`:

- **bug_report.md** — Template for bug reports
  - Environment (Python version, OS)
  - Minimal reproducible example
  - Expected vs actual behavior
  
- **feature_request.md** — Template for feature requests
  - Problem statement
  - Proposed solution
  - Use cases
  
- **documentation.md** — Template for doc improvements
  - Location (file/line)
  - What's missing or unclear
  - Suggested fix

### Contributing Guide

`CONTRIBUTING.md`:
- Dev setup: `pip install -e ".[dev]"`
- Running tests: `pytest tests/ -q`
- Code style: ruff format, mypy strict mode
- PR guidelines: explain "why", link issues, add tests

### Labels & Triage

Standard GitHub labels:
- `good-first-issue` — ~5–10 items for newcomers
- `help-wanted` — soliciting community
- `bug` — defect
- `enhancement` — new feature
- `documentation` — docs improvement
- `question` — usage/clarification

### Response SLA

- **Issues:** 48 hours (reply with clarification or triage)
- **PRs:** 48 hours (review or request changes)
- **Discussions:** Best effort

---

## Phase 20.4: Ecosystem Extras (Planned)

### Optional Dependencies

Already defined in `pyproject.toml`:

```toml
[project.optional-dependencies]
dev = ["pytest", "ruff", "mypy"]           # Development
oracles = ["numpy", "sympy", "networkx"]   # External verification
fast = ["python-flint"]                    # FLINT-backed SNF
gpu = ["cupy-cuda12x"]                     # GPU acceleration
```

Install variants:
```bash
pip install pytop                    # Minimal
pip install pytop[dev]              # Development
pip install pytop[fast]             # FLINT backend
pip install pytop[gpu]              # GPU (CUDA 12.x)
pip install pytop[dev,fast,gpu]     # All
```

---

## Release Timeline

### v1.7.0 (Next Release)

Candidate features from current development:
- Phase 17.2 ✅ (Algorithm optimization)
- Phase 19.1 ✅ (Error message clarity)
- Phase 19.2 (Deprecation infrastructure)

**Target:** 2026-Q3

### v2.0.0 (Major Release)

Breaking changes and deprecations:
- Removal of v1.x deprecations
- New major APIs (if needed)
- Python 3.14+ only (drop 3.11 support)

**Target:** 2027-Q2 (18+ months after v1.0.0)

---

## Success Criteria (Phase 20)

- [ ] **P20.1 ✅** CI/CD hardened (4 Python versions, all checks green)
- [ ] **P20.2** PyPI workflow documented and tested (dry-run on TestPyPI)
- [ ] **P20.3** Contributing guide + issue templates created
- [ ] **P20.4** Ecosystem extras verified (dev/fast/gpu installs work)
- [ ] **Response SLA** 48-hour response on issues/PRs (achievable with 1–2 maintainers)

---

## Maintenance Plan

### Monthly

- Review & close stale issues (60+ days inactive)
- Update dependencies in dev extras
- Spot-check ruff/mypy on latest Python

### Quarterly

- Feature release (e.g., v1.7.0)
- Security audit (dependencies + code)
- Documentation refresh

### Annually

- Deprecation audit (candidates for v2.0.0)
- Performance benchmark refresh
- Community survey (GitHub Discussions)

---

## Quick Links

- **Repository:** https://github.com/kadirhanpolat/pytop
- **Issues:** https://github.com/kadirhanpolat/pytop/issues
- **Discussions:** https://github.com/kadirhanpolat/pytop/discussions
- **CI Workflow:** `.github/workflows/ci.yml`
- **Development:** CLAUDE.md (this repo)
