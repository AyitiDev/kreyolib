import pytest
from kreyolib.normalize import strip_diacritics


def test_strip_diacritics():
    """Test that the function strip all diacritic marks"""
    assert strip_diacritics("") == ""
    assert strip_diacritics("Kilè ou te fè sa?") == "Kile ou te fe sa?"
