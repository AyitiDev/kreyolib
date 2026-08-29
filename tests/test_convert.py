import pytest

from kreyolib.convert.num_to_text import num_to_text
from kreyolib.convert.text_to_num import text_to_num


@pytest.mark.parametrize(
    "input_num, expected",
    [
        (0, "zewo"),
        (0.17, "zewo pwen disèt"),
        (0.014, "zewo pwen zewo katòz"),
        (-5, "mwens senk"),
        (-11, "mwens onz"),
        (12, "douz"),
        (12.4, "douz pwen kat"),
        (20, "ven"),
        (-21, "mwens venteyen"),
        (-157, "mwens san senkannsèt"),
        (21, "venteyen"),
        (-32.1268, "mwens trannde pwen mil de san swasanntuit"),
        (-99, "mwens katrevendisnèf"),
        (223, "de san venntwa"),
        (1001, "mil en"),
        (1001.0, "mil en"),
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


@pytest.mark.parametrize(
    "number, ordinal, error_message",
    [
        (10**24, False, "too large"),
        (-1, True, "must be greater"),
        (3.14, True, "requires a integer"),
    ],
)
def test_num_to_text_guards(number, ordinal, error_message):
    """Test that the function has guards for invalid inputs."""
    with pytest.raises(ValueError, match=error_message):
        num_to_text(number, ordinal=ordinal)


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("mwens de san", -200),
        ("de mil san", 2100),
        ("zewo pwen disèt", 0.17),
        ("mil de sann kenz", 1215),
        ("en pwen krant kat", 1.44),
        ("Krateven disnèf", 99),
        ("katreven diznèf", 99),
        ("zewo pwen zewo uit", 0.08),
        ("mwen sis san mil katrevan", -600080),
        ("sen mil kant san senkant senk", 5455),
        ("kat milyon de san karanntwa", 4_000_243),
    ],
)
def test_text_to_num(input_text, expected):
    """Test that word-formatted text converts back to the correct integer."""
    assert text_to_num(input_text) == expected


@pytest.mark.parametrize(
    "number, error_message",
    [
        ("Sa pa yon chif", "Unrecognized number word"),
        ("Kat mwen dis", "only appear at the start"),
        ("twa pwen twa pwen de", "can only contain one"),
    ],
)
def test_text_to_num_guards(number, error_message):
    """Test that the function has guards for invalid inputs."""
    with pytest.raises(ValueError, match=error_message):
        text_to_num(number)
