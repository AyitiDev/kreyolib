from datetime import datetime, timedelta

import pytest

from kreyolib.convert.datetime_to_text import datetime_to_text
from kreyolib.convert.num_to_text import num_to_text
from kreyolib.convert.text_to_datetime import text_to_datetime
from kreyolib.convert.text_to_num import text_to_num

REFERENCE = datetime(2026, 1, 1)


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
        ("san kat mil", 104000),
        ("mil de san", 1200),
        ("de san mil", 200000),
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
        ("mil mil", "consecutive identical"),
        ("senk senk", "consecutive identical"),
    ],
)
def test_text_to_num_guards(number, error_message):
    """Test that the function has guards for invalid inputs."""
    with pytest.raises(ValueError, match=error_message):
        text_to_num(number)


@pytest.mark.parametrize(
    "input_dt, relative, ref, expected",
    [
        (datetime(2026, 9, 4), False, None, "vandredi 4 septanm 2026"),
        (datetime(2023, 12, 3, 15, 30, 42), False, None, "dimanch 3 desanm 2023, 15:30:42"),
        (-timedelta(weeks=4, days=8), True, None, "sa gen 1 mwa e 5 jou"),
        (timedelta(weeks=12, days=3, hours=60), True, None, "nan 2 mwa, 4 semèn e 12 èdtan"),
        (REFERENCE, True, REFERENCE, "kounye a"),
        (timedelta(days=4), False, REFERENCE, "lendi 5 janvye 2026"),
        (timedelta(hours=5), True, REFERENCE, "jodi a, nan 5 èdtan"),
    ],
)
def test_datetime_to_text(input_dt, relative, ref, expected):
    """Test that datetime/timedelta conversion produces correct Kreyòl text."""
    assert datetime_to_text(input_dt, relative=relative, _ref=ref) == expected


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("2026-01-08 22:33", datetime(2026, 1, 8, 22, 33)),
        ("samdi 1 janvye 2019", datetime(2019, 1, 1)),
        ("2 fevr 2014", datetime(2014, 2, 2)),
        ("sa gen yon ane", datetime(2025, 1, 1)),
        ("sa gen 5 jou, kat semèn", datetime(2025, 11, 29)),
        ("sa gen sèt jou", datetime(2025, 12, 25)),
        ("semèn pase", datetime(2025, 12, 25)),
        ("madi pase", datetime(2025, 12, 31)),
        ("jedi pwochèn", datetime(2026, 1, 8)),
        ("demen", datetime(2026, 1, 2)),
        ("avan yè a 10:45", datetime(2025, 12, 31, 10, 45)),
        ("apre demen a 15è eka", datetime(2026, 1, 3, 15, 15)),
        ("jedi pase a 3è edmi", datetime(2025, 12, 26, 3, 30)),
        ("semèn pwochèn a 10h", datetime(2026, 1, 8, 10)),
        ("mwa kap vini a", datetime(2026, 2, 1)),
        ("demen a dizè", datetime(2026, 1, 2, 10)),
    ],
)
def test_text_to_datetime(input_text, expected):
    """Test that text conversion produces correct datetime."""
    assert text_to_datetime(input_text, _ref=REFERENCE) == expected
