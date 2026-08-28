import pytest

from kreyolib.convert.num_to_text import num_to_text
from kreyolib.convert.text_to_num import text_to_num


@pytest.mark.parametrize(
    "input_num, expected",
    [
        (0, "zewo"),
        (-5, "mwens senk"),
        (-11, "mwens onz"),
        (12, "douz"),
        (20, "ven"),
        (-21, "mwens venteyen"),
        (-157, "mwens san senkannsèt"),
        (21, "venteyen"),
        (-99, "mwens katrevendisnèf"),
        (223, "de san venntwa"),
        (1001, "mil en"),
        (1_000_000, "yon milyon"),
        (400_034, "kat san mil trannkat"),
    ],
)
def test_num_to_text_cardinal(input_num, expected):
    """Test that cardinal conversion produces correct Kreyòl words."""
    assert num_to_text(input_num) == expected


@pytest.mark.parametrize(
    "input_num, expected",
    [
        (1, "premye"),
        (2, "dezyèm"),
        (36, "trannsizyèm"),
        (90, "katrevendizyèm"),
        (12, "douzyèm"),
        (20, "ventyèm"),
        (21, "venteyinyèm"),
        (1001, "mil premye"),
    ],
)
def test_num_to_text_ordinal(input_num, expected):
    """Test that ordinal conversion produces correct Kreyòl words."""
    assert num_to_text(input_num, ordinal=True) == expected


def test_num_to_text_guards():
    """Test that the the function has guard for some cases."""
    # Test that numbers >= 10**24 are out of range.
    with pytest.raises(ValueError, match="too large"):
        num_to_text(10**24)

    # Ordinal form rejects input less than 1
    with pytest.raises(ValueError, match=r"requires a number that is greater"):
        num_to_text(-1, ordinal=True)


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("mwens de san", -200),
        ("de mil san", 2100),
        ("mil de sann kenz", 1215),
        ("Krateven disnèf", 99),
        ("katreven diznèf", 99),
        ("mwen sis san mil katrevan", -600080 ),
        ("sen mil kant san senkant senk", 5455),
        ("kat milyon de san karanntwa", 4_000_243),
    ],
)
def test_text_to_num(input_text, expected):
    """Test that word-formatted text converts back to the correct integer."""
    assert text_to_num(input_text) == expected
