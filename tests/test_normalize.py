import pytest

from kreyolib.normalize import strip_diacritics
from kreyolib.normalize.contractions import expand_contractions


@pytest.mark.parametrize(
    "text_input, expected",
    [
        ("", ""),
        ("Kilè ou te fè sa?", "Kile ou te fe sa?"),
        ("Abèy,èt,òganizasyon", "Abey,et,oganizasyon"),
    ],
)
def test_strip_diacritics(text_input, expected):
    """Test that strip_diacritics correctly removes accent marks."""
    assert strip_diacritics(text_input) == expected


@pytest.mark.parametrize(
    "text_input, expected",
    [
        ("M'ap ale.", "Mwen ap ale."),
        ("Mwen tap di ou l'ap vini.", "Mwen te ap di ou li ap vini."),
        ("Nal travay.", "Nou al travay."),
        ("Y'ap manje.", "Yo ap manje."),
        ("M gen yon map", "Mwen gen yon map"),
        ("Mprale nan fèt la", "Mwen prale nan fèt la"),
    ],
)
def test_expand_contractions(text_input, expected):
    """Test that expand_contractions converts clitics to full words."""
    assert expand_contractions(text_input) == expected
