import pytest

from kreyolib.phonetics.ipa import word_to_ipa
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


@pytest.mark.parametrize(
    "word, expected",
    [
        ("achte", "aʃ.te"),
        ("espesyal", "es.pe.sjal"),
        ("konprann", "kõ.prãn"),
        ("anviwonman", "ã.vi.wõ.mã"),
        ("detwi", "de.twi"),
        ("yo", "jo"),
    ],
)
def test_word_to_ipa(word, expected):
    """Test full word syllabification and IPA transcription with dot boundaries."""
    assert word_to_ipa(word) == expected
