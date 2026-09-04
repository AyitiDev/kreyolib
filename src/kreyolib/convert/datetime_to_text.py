import re
from datetime import datetime, time

WEEKDAYS = [
    "lendi",
    "madi",
    "mèkredi",
    "jedi",
    "vandredi",
    "samdi",
    "dimanch",
]

MONTHS = [
    "janvye",
    "fevriye",
    "mas",
    "avril",
    "me",
    "jen",
    "jiyè",
    "out",
    "septanm",
    "oktòb",
    "novanm",
    "desanm",
]


SECONDS_PER_UNIT = {
    "dekad": 10 * 365 * 24 * 60 * 60,
    "ane": 365 * 24 * 60 * 60,
    "mwa": 30 * 24 * 60 * 60,
    "semèn": 7 * 24 * 60 * 60,
    "jou": 24 * 60 * 60,
    "èdtan": 60 * 60,  # More consistent than `è`
    "minit": 60,
    "segonn": 1,
}

RElATIVE_DAYS = {
    -2: "avan yè",
    -1: "yè",
    0: "jodi a",
    1: "demèn",
    2: "apre demèn",
}


def _convert_to_relative(dt: datetime, max_relative_units: int):
    """Convert a datetime to a relative expression."""
    now = datetime.now()
    delta = now - dt
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
        day_diff = (dt.date() - now.date()).days
        if day_diff in RElATIVE_DAYS:
            prefix = f"{RElATIVE_DAYS[day_diff]}, " + prefix
            parts = parts[1:]

    text = ", ".join([f"{quant} {unit}" for unit, quant in parts])
    return prefix + re.sub(r"\ben", "yon", text)


def date_to_text(
    dt: datetime,
    *,
    relative: bool = False,
    max_relative_units: int = 3,
):
    """Convert a datetime to Haitian Creole text.

    Args:
        dt: Datetime to convert.
        relative: Whether to convert the datetime to a relative
            time expression.
        max_relative_units: Maximum number of non-zero units to
            include in the relative expression.

    Returns:
        A Haitian Creole date, time, or relative-time expression.
    """
    if relative:
        return _convert_to_relative(dt, max_relative_units)

    weekday = WEEKDAYS[dt.weekday()]
    month = MONTHS[dt.month - 1]

    date = f"{weekday} {dt.day} {month} {dt.year}"

    if dt.time() != time.min:
        date += f", {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}"

    return date


if __name__ == "__main__":  # pragma: no cover
    dates = [
        datetime(2026, 9, 4),
        datetime(2026, 9, 4, 15, 30, 42),
        datetime(2026, 9, 3, 23, 59, 30),
    ]

    for dt in dates:
        print(date_to_text(dt))
        print(date_to_text(dt, relative=True))
        print()
