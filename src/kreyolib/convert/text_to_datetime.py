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
from kreyolib.convert.text_to_num import text_to_num

WEEKDAY_CLS = [MO, TU, WE, TH, FR, SA, SU]

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


# fmt: off
class ConversionGrammar(Grammar):
    """Pyleri grammar for Haitian Creole date and time expressions.

    The grammar recognizes calendar dates, relative durations, relative
    units, and relative weekdays.
    """

    t_comma = Token(",")
    t_colon = Token(":")

    r_num = Regex(r"\d+")
    r_num_alpha = Regex(r"[bdekmnostuvy][-_a-zè]*[aefklnstz]")
    r_hour_num = Regex(r"[0-1]?\d|2[0-3]")
    r_minute_num = Regex(r"[0-5]?\d")
    r_day_num = Regex(r"[0-2]?\d|3[01]")
    r_year = Regex(r"\d{4}")
    r_apre = Regex("apr[eè]")
    r_rel_day = Regex(r"jodi\s*y?a|demen|yè")
    r_pwochen = Regex(r"pwoch[eè]n|k['\s]?ap vini an?")

    k_e = Keyword("e")
    k_a = Keyword("a")
    k_h = Choice(Keyword("h"), Keyword("è"))
    k_sa = Keyword("sa")
    k_gen = Keyword("gen")
    k_genyen = Keyword("genyen")
    k_fe = Keyword("fè")
    k_nan = Keyword("nan")
    k_pase = Keyword("pase")
    k_avan = Keyword("avan")
    k_edmi = Keyword("edmi")
    k_eka = Keyword("eka")
    k_article = Choice(Keyword("a"), Keyword("an"))
    k_weekday = Choice(*[Keyword(name) for name in WEEKDAYS])
    k_month = Choice(*[Keyword(name) for name in MONTHS])
    k_unit = Choice(*[Keyword(name) for name in UNITS])

    k_sa_gen = Sequence(k_sa, Choice(k_gen, k_genyen, k_fe))

    op_time = Choice(
        Sequence(k_a, r_hour_num, t_colon, r_minute_num),
        Sequence(
            k_a, r_hour_num, k_h,
            Optional(Choice(r_minute_num, k_edmi, k_eka))
        )
    )

    op_calendar_date = Sequence(
        Optional(
            Sequence(k_weekday, Optional(t_comma))
        ),
        r_day_num, k_month, r_year
    )

    op_relative_date_1 = Sequence(
        Choice(k_sa_gen, k_nan),
        List(
            Sequence(Choice(r_num, r_num_alpha), k_unit),
            delimiter=Choice(t_comma, k_e),
            mi=1
        ),
    )

    op_relative_date_2 = Sequence(
        k_unit,
        Choice(r_pwochen, k_pase),
        Optional(Choice(k_article, op_time)),
    )

    op_relative_day = Sequence(
        Optional(Choice(k_avan, r_apre)),
        r_rel_day,
        Optional(Choice(k_article, op_time)),
    )

    op_relative_weekday = Sequence(
          k_weekday,
          Choice(r_pwochen, k_pase),
          Optional(Choice(k_article, op_time)),
     )

    START = Choice(
        op_calendar_date,
        op_relative_date_1,
        op_relative_date_2,
        op_relative_day,
        op_relative_weekday,
    )
    # fmt: on


class TextToDateTime:
    grm = ConversionGrammar()

    def __init__(self):
        """Initialize the converter and its parser error mappings."""
        self.elem_to_error_msg = {
            self.grm.r_num: "a number (digit)",
            self.grm.r_num_alpha: "a number (alpha)",
            self.grm.r_hour_num: "hour",
            self.grm.r_minute_num: "minute",
            self.grm.r_day_num: "day of the month",
            self.grm.r_year: "year",
            self.grm.r_pwochen: "pwochen/pwochèn",
            self.grm.r_rel_day: "relative day like jodi a, demen, yè ...",
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
                case self.grm.op_relative_day:
                    return self._handle_op_relative_day(op_node.children, ref)
                case self.grm.op_relative_weekday:
                    return self._handle_op_relative_weekday(op_node.children, ref)
                case _:
                    raise NotImplementedError(f"Unhandled operation: {op_node.element.name!r}")

    def _handle_time(self, seq: list) -> timedelta | None:
        """Convert a parsed time operation into a timedelta."""
        item = seq[0].children[0].children
        if item[0].element == self.grm.k_article:
            return None

        time_seq = item[0].children[0].children[1:]

        hours = int(time_seq[0].string)
        minutes = 0
        if len(time_seq) == 3:
            if time_seq[2].string == "eka":
                minutes = 15
            elif time_seq[2].string == "edmi":
                minutes = 30
            else:
                minutes = int(time_seq[2].string)
        return timedelta(hours=hours, minutes=minutes)

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

            count = duration.children[0].string
            unit = duration.children[1].string
            if count.isalpha():
                count = 1 if count in {"yon", "youn"} else text_to_num(count)
            else:
                count = int(count)
            params[UNIT_TRANSLATION[unit]] = count

        return ref + sign * relativedelta(**params)

    def _handle_relative_date_2(self, seq: list, ref: datetime) -> datetime:
        """Convert a relative unit expression into a datetime."""
        if ref is None:
            dt = date.today()
            ref = datetime(dt.year, dt.month, dt.day)

        sign = -1 if seq[1].string == "pase" else 1

        delta = relativedelta(**{UNIT_TRANSLATION[seq[0].string]: sign})
        if len(seq) >= 3 and (time_dt := self._handle_time(seq[2:])):
            delta += time_dt

        return ref + delta

    def _handle_op_relative_day(self, seq: list, ref: datetime) -> datetime:
        """Resolve a relative-day to its nearest matching date."""
        if ref is None:
            dt = date.today()
            ref = datetime(dt.year, dt.month, dt.day)

        prefix = ""
        if seq[0].string.startswith(("ava", "apr")):
            prefix = seq[0].string
            seq = seq[1:]

        if re.match(r"jodi\s*y?a", seq[0].string):
            result = ref
        elif seq[0].string == "yè":
            delta = timedelta(days=-1)
            if prefix == "avan":
                delta = timedelta(days=-2)
            result = ref + delta
        else:
            delta = timedelta(days=1)
            if prefix in {"apre", "aprè"}:
                delta = timedelta(days=2)
            result = ref + delta

        if len(seq) >= 2:
            result += self._handle_time(seq[1:])
        return result

    def _handle_op_relative_weekday(self, seq: list, ref: datetime) -> datetime:
        """Resolve a relative weekday to its nearest matching date."""
        if ref is None:
            dt = date.today()
            ref = datetime(dt.year, dt.month, dt.day)

        sign = -1 if seq[1].string == "pase" else 1
        index = WEEKDAYS_TO_INDEX[seq[0].string]
        weekday_cls = WEEKDAY_CLS[index]
        result = ref + relativedelta(weekday=weekday_cls(sign))

        if result.date() == ref.date():
            result += relativedelta(days=7 * sign)

        if len(seq) >= 3 and (time_dt := self._handle_time(seq[2:])):
            result += time_dt
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


def text_to_datetime(text: str, *, _ref: None | datetime = None) -> datetime:
    """Parse date-like text into a datetime object.

    SupportedFormats:
        Standard numeric datetimes:
            - "2026-01-08 22:33"

        Absolute dates:
            - Day, month, and year: "1 janvye 2019"
            - Day of the week with a date: "samdi 1 janvye 2019"

        Relative dates:
            - Relative days: "demen", "apre demen"
            - Previous or next periods: "semèn pase",
              "semèn pwochèn", "mwa kap vini a"
            - Previous or next weekdays: "madi pase",
              "jedi pase"

        Relative durations:
            - Past durations: "sa gen 5 jou"
            - Multiple past durations: "sa gen 5 jou, kat semèn"

        Time expressions:
            - Hours and minutes can be combined with date expressions:
              "demen a 15è eka", "jedi pase a 3è edmi",
              "semèn pwochèn a 10h".

    Args:
        text: Text containing a date, relative date, duration, or timestamp.
        _ref: Internal reference datetime used for resolving relative
            expressions and deterministic testing.

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

    return _converter.translate(text, _ref)


if __name__ == "__main__":  # pragma: no cover
    texts = [
        "2026-01-08 22:33",
        "sa gen yon mwa",
        "samdi 1 janvye 2019",
        "sa gen 5 jou, 4 semèn",
        "sa gen sèt ane",
        "semèn pwochèn a 10h",
        "jedi pase a 3è edmi",
        "apre demen a 15è eka",
        "mwa kap vini a",
    ]
    for text in texts:
        print(f"{text}:", text_to_datetime(text, _ref=datetime(2026, 1, 1)))
