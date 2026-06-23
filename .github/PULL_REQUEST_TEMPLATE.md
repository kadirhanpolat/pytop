<!-- Thanks for contributing to pytop! Keep the description focused on the math and the change. -->

## Summary

<!-- What does this PR do, and why? Reference the phase/milestone if applicable (e.g. P17.3). -->

## Type of change

- [ ] Bug fix (non-breaking)
- [ ] New feature (non-breaking)
- [ ] Performance (behavior-preserving)
- [ ] Breaking change (requires a deprecation entry — see `DEPRECATIONS.md`)
- [ ] Docs only

## Validation

<!-- How do you know the result is correct? Pick all that apply. -->

- [ ] Known-answer tests (textbook/hand computation)
- [ ] Cross-checked against an external oracle (GUDHI / SnapPy / Sage / networkx / numpy)
- [ ] Property-based / invariant tests
- [ ] Output is byte-identical to the previous implementation (perf PRs)

## Checklist

- [ ] `pytest tests/ -q` passes locally (`py -3.14 -m pytest`)
- [ ] `ruff check src/ tests/` is clean
- [ ] `mypy src/pytop` is clean
- [ ] New public symbols are exported from `src/pytop/__init__.py`
- [ ] `CHANGELOG.md` updated for any behavior change
- [ ] `__version__` and `pyproject.toml` version stay in sync (if bumped)
- [ ] No new runtime dependencies added to `src/pytop/`
