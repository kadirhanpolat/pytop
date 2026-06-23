"""Internal deprecation utilities (P19.2).

A single reusable ``@deprecated`` decorator so every deprecation in pytop emits a
consistent, actionable :class:`DeprecationWarning` and documents itself the same
way. The message follows the project's WHY-HOW-THEN pattern:

* **WHY**  -- ``<name>`` is deprecated since ``<since>``.
* **HOW**  -- it will be removed in ``<removed_in>`` (the 18-month window).
* **THEN** -- use ``<alternative>`` instead.

This module is internal (underscore-prefixed, not exported from ``__init__``).
Apply it at definition sites inside the package; see ``DEPRECATIONS.md`` for the
registry and policy.
"""

from __future__ import annotations

import functools
import warnings
from collections.abc import Callable
from typing import TypeVar

__all__ = ["deprecated", "deprecation_message"]

T = TypeVar("T", bound=Callable[..., object])


def deprecation_message(
    name: str,
    *,
    since: str,
    removed_in: str,
    alternative: str | None = None,
    reason: str | None = None,
) -> str:
    """Build the canonical WHY-HOW-THEN deprecation message for ``name``."""
    parts = [
        f"{name} is deprecated since pytop {since} and will be removed in {removed_in}."
    ]
    if alternative:
        parts.append(f"Use {alternative} instead.")
    if reason:
        parts.append(reason)
    return " ".join(parts)


def deprecated(
    *,
    since: str,
    removed_in: str,
    alternative: str | None = None,
    reason: str | None = None,
) -> Callable[[T], T]:
    """Mark a function or class as deprecated.

    Emits a :class:`DeprecationWarning` on call (for functions) or on
    instantiation (for classes), and prepends a ``.. deprecated::`` note to the
    object's docstring so the deprecation is visible in help() and Sphinx.

    Parameters
    ----------
    since:
        Version the deprecation took effect, e.g. ``"1.7.0"``.
    removed_in:
        Version the symbol will be removed, e.g. ``"2.0.0"`` (18-month window).
    alternative:
        The replacement to point users to, e.g. ``"persistence_pairs_twist"``.
    reason:
        Optional extra context appended to the message.

    Example
    -------
    >>> @deprecated(since="1.7.0", removed_in="2.0.0", alternative="new_fn")
    ... def old_fn():
    ...     ...
    """

    def decorate(obj: T) -> T:
        name = getattr(obj, "__qualname__", getattr(obj, "__name__", repr(obj)))
        message = deprecation_message(
            name,
            since=since,
            removed_in=removed_in,
            alternative=alternative,
            reason=reason,
        )
        note = (
            f"\n\n.. deprecated:: {since}\n"
            f"   Removed in {removed_in}."
            + (f" Use :func:`{alternative}` instead." if alternative else "")
        )

        if isinstance(obj, type):
            original_init = obj.__init__  # type: ignore[misc]

            @functools.wraps(original_init)
            def init_wrapper(self: object, *args: object, **kwargs: object) -> None:
                warnings.warn(message, DeprecationWarning, stacklevel=2)
                original_init(self, *args, **kwargs)

            obj.__init__ = init_wrapper  # type: ignore[misc]
            obj.__doc__ = (obj.__doc__ or "") + note
            return obj

        @functools.wraps(obj)
        def func_wrapper(*args: object, **kwargs: object) -> object:
            warnings.warn(message, DeprecationWarning, stacklevel=2)
            return obj(*args, **kwargs)

        func_wrapper.__doc__ = (func_wrapper.__doc__ or "") + note
        # Expose the metadata for tooling / DEPRECATIONS.md generation.
        func_wrapper.__deprecated__ = {  # type: ignore[attr-defined]
            "since": since,
            "removed_in": removed_in,
            "alternative": alternative,
        }
        return func_wrapper  # type: ignore[return-value]

    return decorate
