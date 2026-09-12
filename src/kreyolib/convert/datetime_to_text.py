import re
from datetime import datetime, time, timedelta

from kreyolib.convert._datetime_vocab import MONTHS, SECONDS_PER_UNIT, WEEKDAYS


def _format_relative_seq(prefix: str, parts: list) -> str:
    """Format a sequence of relative time components into natural language."""
    if len(parts) == 1:
        text = f"{parts[0][1]} {parts[0][0]}"
    else:
        str_parts = [f"{quant} {unit}" for unit, quant in parts]
        text = f"{', '.join(str_parts[:-1])} e {str_parts[-1]}"
    return prefix + re.sub(r"\ben", "yon", text)


def _convert_to_relative(
    dt: datetime | timedelta,
    ref: datetime,
    max_relative_units: int,
) -> str:
    """Convert a datetime to a relative expression."""
    if isinstance(dt, timedelta):
        dt = ref + dt

    delta = ref - dt
    remaining_sec = abs(delta.total_seconds())

    if remaining_sec < 1:
        return "kounye a"

    prefix = "nan " if delta.total_seconds() < 0 else "sa gen "

    parts = []
    for unit, unit_seconds in SECONDS_PER_UNIT.items():
        quantity, remaining_sec = divmod(remaining_sec, unit_seconds)
        quantity = int(quantity)

        if quantity:
            parts.append((unit, quantity))

        if len(parts) == max_relative_units:
            break

    if parts[0][0] in {"èdtan", "minit", "segonn"}:
        day_diff = dt.days if isinstance(dt, timedelta) else (dt.date() - ref.date()).days
        if day_diff == 0:
            prefix = "jodi a, " + prefix

    return _format_relative_seq(prefix, parts)


def datetime_to_text(
    dt: datetime | timedelta,
    *,
    relative: bool = False,
    max_relative_units: int = 3,
    _ref: None | datetime = None,
) -> str:
    """Convert a datetime to Haitian Creole text.

    Args:
        dt: Datetime or timedelta object to convert.
        relative: Whether to convert the datetime to a relative
            time expression.
        max_relative_units: Maximum number of non-zero units to
            include in the relative expression.
        _ref: Internal param to allow deterministic testing.

    Returns:
        A Haitian Creole date, time, or relative-time expression.
    """
    ref = _ref or datetime.now()
    if relative:
        return _convert_to_relative(dt, ref, max_relative_units)

    if isinstance(dt, timedelta):
        dt += ref

    weekday = WEEKDAYS[dt.weekday()]
    month = MONTHS[dt.month - 1]

    date = f"{weekday} {dt.day} {month} {dt.year}"

    if dt.time() != time.min:
        date += f", {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}"

    return date


if __name__ == "__main__":  # pragma: no cover
    dates = [
        datetime.now(),
        datetime(2026, 9, 4),
        datetime(2026, 9, 8, 23, 59, 30),
        datetime(2023, 12, 3, 15, 30, 42),
        timedelta(weeks=12, days=3, hours=60),
    ]
    for dt in dates:
        print("abs:", datetime_to_text(dt))
        print("rel:", datetime_to_text(dt, relative=True))
        print()
