import re
from datetime import datetime, time, timedelta

from kreyolib.convert._datetime_vocab import MONTHS, SECONDS_PER_UNIT, WEEKDAYS, RElATIVE_DAYS


def _convert_to_relative(
    dt: datetime | timedelta,
    reference: datetime,
    max_relative_units: int,
):
    """Convert a datetime to a relative expression."""
    delta = dt if isinstance(dt, timedelta) else reference - dt
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

    if parts[0][0] in {"jou", "èdtan", "minit", "segonn"}:
        day_diff = (
            dt.days if isinstance(dt, timedelta) else (dt.date() - reference.date()).days
        )
        if day_diff in RElATIVE_DAYS:
            prefix = f"{RElATIVE_DAYS[day_diff]}, " + prefix

    text = ", ".join([f"{quant} {unit}" for unit, quant in parts])
    return prefix + re.sub(r"\ben", "yon", text)


def datetime_to_text(
    dt: datetime | timedelta,
    *,
    relative: bool = False,
    max_relative_units: int = 3,
    _ref=None,
):
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
    reference = _ref or datetime.now()
    if relative:
        return _convert_to_relative(dt, reference, max_relative_units)

    if isinstance(dt, timedelta):
        dt += reference

    weekday = WEEKDAYS[dt.weekday()]
    month = MONTHS[dt.month - 1]

    date = f"{weekday} {dt.day} {month} {dt.year}"

    if dt.time() != time.min:
        date += f", {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}"

    return date


if __name__ == "__main__":  # pragma: no cover
    dates = [
        datetime(2026, 9, 4),
        datetime(2023, 12, 3, 15, 30, 42),
        datetime(2026, 9, 3, 23, 59, 30),
        timedelta(weeks=12, days=3, hours=60),
    ]

    for dt in dates:
        print(datetime_to_text(dt))
        print(datetime_to_text(dt, relative=True))
        print()
