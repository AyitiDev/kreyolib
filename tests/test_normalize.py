import pytest

from kreyolib.normalize import strip_diacritics
from kreyolib.normalize.contractions import expand_contractions
from kreyolib.normalize.orthography import standardize_text


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


@pytest.mark.parametrize(
    "text_input, aggressive, expected",
    [
        # Test that non-aggressive mode preserves some French names
        (
            "Dénise pral lakay li.",
            False,
            "Dénise pral lakay li.",
        ),
        # Test article correction
        (
            "mwen chita sou ban a. Mwen ap manje bannann la ki te sou tab lan.",
            False,
            "Mwen chita sou ban an. Mwen ap manje bannann nan ki te sou tab la.",
        ),
        # Test chat abbreviation expansion
        (
            "Bjr! Mw tap tann ou. svp chr ou knn c fèt mwen",
            False,
            "Bonjou! Mwen tap tann ou. silvouplè cheri ou konn se fèt mwen",
        ),
        # Test aggressive vocabulary mapping
        (
            "Nan lé monn mouin té pèdu nan péché; Min Jézu té sové-m, map rann gloua a li.",
            True,
            "Nan le mond mwen te pèdi nan peche; Men Jezi te sovem, map rann glwa a li.",
        ),
        # Test that lowercase of Jesus if fixed
        ("Jezi ak bondye", False, "Jezi ak Bondye"),
    ],
)
def test_standardize_text_variations(text_input, aggressive, expected):
    """Test behavior across different params, phrases, and aggressiveness levels."""
    assert standardize_text(text_input, aggressive=aggressive) == expected
