import pytest

from kreyolib.phonetics.syllable import syllabify


@pytest.mark.parametrize(
    "word_input, expected",
    [
        ("lè", ["lè"]),
        ("ui", ["ui"]),
        ("uit", ["uit"]),
        ("uitè", ["ui", "tè"]),
        ("pwente", ["pwen", "te"]),
        ("achte", ["ach", "te"]),
        ("prepare", ["pre", "pa", "re"]),
        ("espesyal", ["es", "pe", "syal"]),
        ("konprann", ["kon", "prann"]),
        ("bannann", ["ban", "nann"]),
        ("detwi", ["de", "twi"]),
        ("chanm", ["chanm"]),
        ("jwèt", ["jwèt"]),
        ("apwoche", ["a", "pwo", "che"]),
        ("televizyon", ["te", "le", "vi", "zyon"]),
        ("anviwonman", ["an", "vi", "won", "man"]),
        ("espyon", ["es", "pyon"]),
    ],
)
def test_syllabify(word_input, expected):
    """Test that words are split to the correct syllables."""
    assert syllabify(word_input) == expected
