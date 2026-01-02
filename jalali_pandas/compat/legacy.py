"""Legacy API compatibility for jalali-pandas v0.x.

This module provides backward compatibility for the v0.x API.
Users migrating from v0.x should use the new API but can continue
using the old API with deprecation warnings.
"""

from __future__ import annotations

import warnings
from functools import wraps
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def deprecated(
    old_name: str,
    new_name: str | None = None,
    version: str = "1.0.0",
    removal_version: str = "2.0.0",
) -> Callable[[F], F]:
    """Decorator to mark functions/methods as deprecated.

    Args:
        old_name: The old function/method name.
        new_name: The new function/method name (if renamed).
        version: Version when deprecation was introduced.
        removal_version: Version when the old API will be removed.

    Returns:
        Decorated function that emits deprecation warning.
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if new_name:
                msg = (
                    f"'{old_name}' is deprecated since version {version} "
                    f"and will be removed in version {removal_version}. "
                    f"Use '{new_name}' instead."
                )
            else:
                msg = (
                    f"'{old_name}' is deprecated since version {version} "
                    f"and will be removed in version {removal_version}."
                )
            warnings.warn(msg, FutureWarning, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


class DeprecatedAlias:
    """Descriptor for deprecated class aliases."""

    def __init__(
        self,
        target_class: type,
        old_name: str,
        new_name: str,
        version: str = "1.0.0",
        removal_version: str = "2.0.0",
    ) -> None:
        """Initialize deprecated alias.

        Args:
            target_class: The actual class to use.
            old_name: The old class name.
            new_name: The new class name.
            version: Version when deprecation was introduced.
            removal_version: Version when the old API will be removed.
        """
        self._target_class = target_class
        self._old_name = old_name
        self._new_name = new_name
        self._version = version
        self._removal_version = removal_version

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Create instance with deprecation warning."""
        warnings.warn(
            f"'{self._old_name}' is deprecated since version {self._version} "
            f"and will be removed in version {self._removal_version}. "
            f"Use '{self._new_name}' instead.",
            FutureWarning,
            stacklevel=2,
        )
        return self._target_class(*args, **kwargs)


def emit_deprecation_warning(
    old_name: str,
    new_name: str | None = None,
    version: str = "1.0.0",
    removal_version: str = "2.0.0",
) -> None:
    """Emit a deprecation warning.

    Args:
        old_name: The old API name.
        new_name: The new API name (if renamed).
        version: Version when deprecation was introduced.
        removal_version: Version when the old API will be removed.
    """
    if new_name:
        msg = (
            f"'{old_name}' is deprecated since version {version} "
            f"and will be removed in version {removal_version}. "
            f"Use '{new_name}' instead."
        )
    else:
        msg = (
            f"'{old_name}' is deprecated since version {version} "
            f"and will be removed in version {removal_version}."
        )
    warnings.warn(msg, FutureWarning, stacklevel=3)


__all__ = [
    "deprecated",
    "DeprecatedAlias",
    "emit_deprecation_warning",
]
