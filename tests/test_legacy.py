"""Tests for legacy compatibility module."""

from __future__ import annotations

import pytest

from jalali_pandas.compat.legacy import (
    DeprecatedAlias,
    deprecated,
    emit_deprecation_warning,
)


class TestDeprecatedDecorator:
    """Tests for the deprecated decorator."""

    def test_deprecated_function_emits_warning(self) -> None:
        """Test that deprecated decorator emits FutureWarning."""

        @deprecated("old_func", "new_func")
        def old_func() -> str:
            return "result"

        with pytest.warns(FutureWarning, match="'old_func' is deprecated"):
            result = old_func()

        assert result == "result"

    def test_deprecated_warning_message_with_new_name(self) -> None:
        """Test warning message includes new name."""

        @deprecated("old_func", "new_func", version="1.0.0", removal_version="2.0.0")
        def old_func() -> str:
            return "result"

        with pytest.warns(FutureWarning) as record:
            old_func()

        assert len(record) == 1
        assert "'old_func' is deprecated since version 1.0.0" in str(record[0].message)
        assert "will be removed in version 2.0.0" in str(record[0].message)
        assert "Use 'new_func' instead" in str(record[0].message)

    def test_deprecated_warning_message_without_new_name(self) -> None:
        """Test warning message when no new name is provided."""

        @deprecated("old_func", version="1.0.0", removal_version="2.0.0")
        def old_func() -> str:
            return "result"

        with pytest.warns(FutureWarning) as record:
            old_func()

        assert len(record) == 1
        assert "'old_func' is deprecated since version 1.0.0" in str(record[0].message)
        assert "Use" not in str(record[0].message)

    def test_deprecated_preserves_function_metadata(self) -> None:
        """Test that deprecated decorator preserves function metadata."""

        @deprecated("my_func", "new_func")
        def my_func() -> str:
            """My docstring."""
            return "result"

        assert my_func.__name__ == "my_func"
        assert my_func.__doc__ == "My docstring."

    def test_deprecated_with_arguments(self) -> None:
        """Test deprecated function with arguments."""

        @deprecated("add", "new_add")
        def add(a: int, b: int) -> int:
            return a + b

        with pytest.warns(FutureWarning):
            result = add(2, 3)

        assert result == 5

    def test_deprecated_with_kwargs(self) -> None:
        """Test deprecated function with keyword arguments."""

        @deprecated("greet", "new_greet")
        def greet(name: str, greeting: str = "Hello") -> str:
            return f"{greeting}, {name}!"

        with pytest.warns(FutureWarning):
            result = greet("World", greeting="Hi")

        assert result == "Hi, World!"


class TestDeprecatedAlias:
    """Tests for DeprecatedAlias class."""

    def test_deprecated_alias_emits_warning(self) -> None:
        """Test that DeprecatedAlias emits warning on instantiation."""

        class NewClass:
            def __init__(self, value: int) -> None:
                self.value = value

        OldClass = DeprecatedAlias(NewClass, "OldClass", "NewClass")

        with pytest.warns(FutureWarning, match="'OldClass' is deprecated"):
            obj = OldClass(42)

        assert obj.value == 42

    def test_deprecated_alias_warning_message(self) -> None:
        """Test warning message from DeprecatedAlias."""

        class NewClass:
            pass

        OldClass = DeprecatedAlias(
            NewClass, "OldClass", "NewClass", version="1.0.0", removal_version="2.0.0"
        )

        with pytest.warns(FutureWarning) as record:
            OldClass()

        assert len(record) == 1
        assert "'OldClass' is deprecated since version 1.0.0" in str(record[0].message)
        assert "Use 'NewClass' instead" in str(record[0].message)


class TestEmitDeprecationWarning:
    """Tests for emit_deprecation_warning function."""

    def test_emit_warning_with_new_name(self) -> None:
        """Test emitting warning with new name."""
        with pytest.warns(FutureWarning) as record:
            emit_deprecation_warning("old_api", "new_api")

        assert len(record) == 1
        assert "'old_api' is deprecated" in str(record[0].message)
        assert "Use 'new_api' instead" in str(record[0].message)

    def test_emit_warning_without_new_name(self) -> None:
        """Test emitting warning without new name."""
        with pytest.warns(FutureWarning) as record:
            emit_deprecation_warning("old_api")

        assert len(record) == 1
        assert "'old_api' is deprecated" in str(record[0].message)
        assert "Use" not in str(record[0].message)

    def test_emit_warning_custom_versions(self) -> None:
        """Test emitting warning with custom versions."""
        with pytest.warns(FutureWarning) as record:
            emit_deprecation_warning(
                "old_api", "new_api", version="0.9.0", removal_version="1.5.0"
            )

        assert "since version 0.9.0" in str(record[0].message)
        assert "removed in version 1.5.0" in str(record[0].message)
