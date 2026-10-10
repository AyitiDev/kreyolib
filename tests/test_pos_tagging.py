import pytest

from kreyolib.tagger.pos import tag


@pytest.mark.parametrize(
    ("inputs, expected"),
    [
        ("", []),
        (
            "Map vini demen nan maten.",
            [
                ("M", "PRON"),
                ("ap", "AUX"),
                ("vini", "VERB"),
                ("demen", "NOUN"),
                ("nan", "ADP"),
                ("maten", "NOUN"),
                (".", "PUNCT"),
            ],
        ),
        (
            "Lap travay pandan tout jounen an.",
            [
                ("L", "PRON"),
                ("ap", "AUX"),
                ("travay", "VERB"),
                ("pandan", "ADP"),
                ("tout", "DET"),
                ("jounen", "NOUN"),
                ("an", "DET"),
                (".", "PUNCT"),
            ],
        ),
        (
            ["Mwen", "rele", "Jan", ",", "e", "mwen", "abite", "Okay", "."],
            [
                ("Mwen", "PRON"),
                ("rele", "VERB"),
                ("Jan", "PROPN"),
                (",", "PUNCT"),
                ("e", "CCONJ"),
                ("mwen", "PRON"),
                ("abite", "VERB"),
                ("Okay", "NOUN"),
                (".", "PUNCT"),
            ],
        ),
        (
            ["Li", "se", "Christophe", "."],
            [
                ("Li", "PRON"),
                ("se", "VERB"),
                ("Christophe", "PROPN"),
                (".", "PUNCT"),
            ],
        ),
        (
            "Kisak fè sa?",
            [
                ("Kisa", "PRON"),
                ("k", "SCONJ"),
                ("fè", "VERB"),
                ("sa", "PRON"),
                ("?", "PUNCT"),
            ],
        ),
        (
            "na fè sa pita",
            [
                ("nou", "PRON"),
                ("a", "AUX"),
                ("fè", "VERB"),
                ("sa", "PRON"),
                ("pita", "NOUN"),
            ],
        ),
        (
            "Ma vini demen.",
            [
                ("Mwen", "PRON"),
                ("a", "AUX"),
                ("vini", "VERB"),
                ("demen", "NOUN"),
                (".", "PUNCT"),
            ],
        ),
        (
            "Ou te di m wa gentan vini.",
            [
                ("Ou", "PRON"),
                ("te", "AUX"),
                ("di", "VERB"),
                ("m", "PRON"),
                ("ou", "PRON"),
                ("a", "AUX"),
                ("gentan", "ADV"),
                ("vini", "VERB"),
                (".", "PUNCT"),
            ],
        ),
    ],
)
def test_pos_tagging(inputs, expected):
    """Test POS tagger with extended string and tokenized inputs."""
    assert tag(inputs) == expected
