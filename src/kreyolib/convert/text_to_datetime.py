import re
from datetime import date, datetime, timedelta

import dateutil
from dateutil.relativedelta import FR, MO, SA, SU, TH, TU, WE, relativedelta
from pyleri import (
    Choice,
    Grammar,
    Keyword,
    List,
    Optional,
    Regex,
    Sequence,
    Token,
    end_of_statement,
)

from kreyolib.convert._datetime_vocab import (
    MONTHS,
    MONTHS_TO_INDEX,
    UNIT_TRANSLATION,
    UNITS,
    WEEKDAYS,
    WEEKDAYS_TO_INDEX,
)

WEEKDAY_CLS = [MO, TU, WE, TH, FR, SA, SU]

RELATIVE_DAYS = {
    "avan yè": -2,
    "yè": -1,
    "jodi a": 0,
    "demen": 1,
    "aprè demèn": 2,
}
RELATIVE_DAYS_PATTERN = re.compile(rf"\b(?:{'|'.join(RELATIVE_DAYS)})")

_converter = None


def _looks_datetime_like(text: str) -> bool:
    """Check whether text has a numeric structure resembling a date or timestamp.

    Args:
        text: Text to inspect.

    Returns:
        True if more than 80% of alphanumeric characters are numeric,
        otherwise False.
    """
    chars = [char for char in text if char.isalnum()]

    if not chars:
        return False

    numeric = sum(char.isdigit() for char in chars)

    return numeric / len(chars) > 0.8


def _relative_day_to_date(rel_day: str, ref: datetime) -> datetime:
    """Convert a relative-day expression into an absolute date.

    Args:
        rel_day: Haitian Creole relative-day expression such as
            ``"yè"`` or ``"demen"``.
        _ref: Internal param to allow deterministic testing.

    Returns:
        The date corresponding to the relative-day expression.

    Raises:
        KeyError: If ``rel_day`` is not a supported relative-day expression.
    """
    ref = ref or date.today()
    day_diff = RELATIVE_DAYS[rel_day]
    return ref + timedelta(days=day_diff)


class ConversionGrammar(Grammar):
    """Pyleri grammar for Haitian Creole date and time expressions.

    The grammar recognizes calendar dates, relative durations, relative
    units, and relative weekdays.
    """

    t_comma = Token(",")

    r_num = Regex(r"\d+")
    r_month_num = Regex(r"\d{1,2}")
    r_year = Regex(r"\d{4}")
    r_pwochen = Regex(r"pwoch[eè]n")

    k_e = Keyword("e")
    k_sa = Keyword("sa")
    k_gen = Keyword("gen")
    k_genyen = Keyword("genyen")
    k_fe = Keyword("fè")
    k_nan = Keyword("nan")
    k_pase = Keyword("pase")
    k_article = Choice(Keyword("a"), Keyword("an"))

    k_weekday = Choice(*[Keyword(name) for name in WEEKDAYS])
    k_month = Choice(*[Keyword(name) for name in MONTHS])
    k_unit = Choice(*[Keyword(name) for name in UNITS])

    k_sa_gen = Sequence(k_sa, Choice(k_gen, k_genyen, k_fe))

    op_calendar_date = Sequence(
        Optional(Sequence(k_weekday, Optional(t_comma))), r_month_num, k_month, r_year
    )

    op_relative_date_1 = Sequence(
        Choice(k_sa_gen, k_nan),
        List(Sequence(r_num, k_unit), delimiter=Choice(t_comma, k_e), mi=1),
    )

    op_relative_date_2 = Sequence(k_unit, Choice(r_pwochen, k_pase), Optional(k_article))

    op_relative_weekday = Sequence(k_weekday, Choice(r_pwochen, k_pase), Optional(k_article))

    START = Choice(
        op_calendar_date,
        op_relative_date_1,
        op_relative_date_2,
        op_relative_weekday,
    )


class TextToDateTime:
    grm = ConversionGrammar()

    def __init__(self):
        """Initialize the converter and its parser error mappings."""
        self.elem_to_error_msg = {
            self.grm.r_num: "number",
            self.grm.r_month_num: "month number",
            self.grm.r_year: "year",
        }

    def translate(self, text: str, ref: datetime) -> datetime:
        """Parse a Haitian Creole date expression into a datetime."""
        res = self.grm.parse(text)
        if not res.is_valid:
            raise ValueError(self._build_error_msg(res))

        for op_node in res.tree.children[0].children:
            match op_node.element:
                case self.grm.op_calendar_date:
                    return self._handle_calendar_date(op_node.children)
                case self.grm.op_relative_date_1:
                    return self._handle_relative_date_1(op_node.children, ref)
                case self.grm.op_relative_date_2:
                    return self._handle_relative_date_2(op_node.children, ref)
                case self.grm.op_relative_weekday:
                    return self._handle_op_relative_weekday(op_node.children, ref)
                case _:
                    raise NotImplementedError(f"Unhandled operation: {op_node.element.name!r}")

    def _handle_calendar_date(self, seq: list) -> datetime:
        """Convert a parsed calendar-date operation into a datetime."""
        cleaned_seq = [s for s in seq if not isinstance(s.element, Optional)]

        day = int(cleaned_seq[0].string)
        month = MONTHS_TO_INDEX[cleaned_seq[1].string]
        year = int(cleaned_seq[2].string)
        return datetime(year, month, day)

    def _handle_relative_date_1(self, seq: list, ref: datetime) -> datetime:
        """Convert a relative duration expression into a datetime."""
        ref = ref or datetime.now()
        sign = -1 if seq[0].children[0].element is self.grm.k_sa_gen else 1

        params = {}
        for duration in seq[1].children:
            if duration.string in {",", "e"}:
                continue

            count, unit = duration.children
            params[UNIT_TRANSLATION[unit.string]] = int(count.string)

        return ref + sign * relativedelta(**params)

    def _handle_relative_date_2(self, seq: list, ref: datetime) -> datetime:
        """Convert a relative unit expression into a datetime."""
        ref = ref or datetime.now()
        sign = -1 if seq[1].string == "pase" else 1

        delta = relativedelta(**{UNIT_TRANSLATION[seq[0].string]: sign})

        return ref + delta

    def _handle_op_relative_weekday(self, seq: list, ref: datetime) -> datetime:
        """Resolve a relative weekday to its nearest matching date."""
        sign = -1 if seq[1].string == "pase" else 1
        ref = ref or datetime.now()

        index = WEEKDAYS_TO_INDEX[seq[0].string]
        weekday_cls = WEEKDAY_CLS[index]
        result = ref + relativedelta(weekday=weekday_cls(sign))

        if result.date() == ref.date():
            result += relativedelta(days=7 * sign)

        return result

    def _build_error_msg(self, res) -> str:
        """Build a human-readable parser error message."""
        err_msg = f"error at pos {res.pos}"

        expecting_list = []
        for elem in res.expecting:
            expect = self.elem_to_error_msg.get(elem)
            if expect is None and isinstance(elem, (Keyword, Token)):
                expect = str(elem)
            elif elem is end_of_statement:
                expect = "end of statement"

            if expect:
                expecting_list.append(expect)

        expecting_list.sort()

        if len(expecting_list) == 1:
            err_msg += f", expecting: {expecting_list[0]}"
        elif len(expecting_list) >= 2:
            err_msg += f", expecting: {', '.join(expecting_list[:-1])} or {expecting_list[-1]}"

        return err_msg


def text_to_datetime(text: str, *, _ref=None | datetime) -> datetime:
    """Parse date-like text into a datetime object.

    SupportedFormats:
        ...

    Args:
        text: Text containing a date or timestamp.
        _ref: Internal param to allow deterministic testing.

    Returns:
        A datetime object parsed from the input text.

    Raises:
        ValueError: If the text cannot be parsed as a datetime.
    """
    global _converter
    if _converter is None:
        _converter = TextToDateTime()

    text = text.lower()

    if _looks_datetime_like(text):
        try:
            return dateutil.parser.parse(text)
        except (ValueError, OverflowError) as exc:
            raise ValueError(f"Invalid datetime: {text!r}") from exc

    m = RELATIVE_DAYS_PATTERN.search(text)
    # This covers case like "demen 15 jen 2019"
    if m:
        rel_day = m.group()
        rem_text = text[: m.start()] + text[m.end() :]
        date_part = _relative_day_to_date(rel_day, _ref)
        if rem_text.strip():
            return date_part + _converter.translate(rem_text)
        return date_part

    return _converter.translate(text, _ref)


if __name__ == "__main__":  # pragma: no cover
    texts = [
        "samdi 1 janvye 2019",
        "sa gen 5 jou, 4 semèn",
        "semèn pase",
        "madi pase",
    ]
    for text in texts:
        print(f"{text}:", text_to_datetime(text))
