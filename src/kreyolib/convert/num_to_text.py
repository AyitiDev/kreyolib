import re
from decimal import Decimal

from kreyolib.convert._vocab import IRREG_ORDINAL_MAP, NUM_TO_TEXT, SCALES, TEXT_TO_NUM

# Scales that ussualy take the prefix `yon`
# When the magnitude is one, e.g., yon milyon.
EXCEPTIONS_SCALES = SCALES - {"san", "mil"}

# Detection regex to detect the first 4 cardinal num
# Since they can also merged with some into some number
FIRST_CARDINALS_DETECTOR = re.compile(r"(?:[yv]?en|de|twa|kat|nèf|[sd]is)$")


def _finalize(seq: list[str], *, ordinal: bool) -> str:
    """Apply ordinal conversion, decimal point, and the yon prefix."""
    if ordinal:
        last_token = seq[-1]
        m = FIRST_CARDINALS_DETECTOR.search(last_token)
        if m:
            seq[-1] = last_token[: m.start()] + IRREG_ORDINAL_MAP[m.group(0)]
        else:
            seq[-1] += "yèm"
        return " ".join(seq)

    text = " ".join(seq)
    return "yon " + text if seq[0] in EXCEPTIONS_SCALES else text


def _num_to_text_seq(input_num: int) -> list[str]:
    # Quick path
    if input_num in NUM_TO_TEXT:
        return [NUM_TO_TEXT[input_num]]

    sequence = []
    for text, num in TEXT_TO_NUM.items():
        # Prevent ZeroDivisionError
        # It is the end of the map anyway
        if num == 0:
            break

        # Count = magnitude: 0 = nothing
        # e.g., for 42_000, q = 42
        count, input_num = divmod(input_num, num)
        if count == 0:
            pass
        elif count == 1:
            sequence.append(text)
        else:
            sequence.append(f"{num_to_text(count)} {text}")

    return sequence


def num_to_text(input_num: int, *, ordinal: bool = False) -> str:
    """Convert an integer into its Kreyòl word representation.

    Uses a greedy decomposition over the magnitude map (units up to
    trilya = 10**21) and recursively converts the count of each magnitude.
    Powers of a thousand (mil, milyon, ...) are prefixed with "yon" when the
    count is one (e.g. 1_000_000 -> "yon milyon").

    Args:
        input_num: The integer to convert.
        ordinal: If True, return the ordinal form (e.g. "premye",
            "dezyèm") instead of the cardinal form.

    Returns:
        The Kreyòl word form of the number.

    Raises:
        ValueError: If input_num is greater than or equal to 10**24, or if
            ordinal is True and input_num is less than 1.
    """
    if ordinal and (isinstance(input_num, float) or input_num < 1):
        raise ValueError("ordinal form requires a integer and must be greater than zero")

    sequence = []
    if input_num < 0:
        sequence.append("mwens")
    input_num = abs(input_num)

    if input_num >= 10**24:
        raise ValueError(f"number too large. Maximum supported is 10**24 - 1, got {input_num}")
    whole = round(input_num)
    sequence += _num_to_text_seq(whole)

    decimal_part = Decimal(str(input_num)) % 1
    if not decimal_part:
        return _finalize(sequence, ordinal=ordinal)

    target = str(decimal_part).split(".")[1]  # e.g., 0.014 = 014
    fract_digits = int(target)
    leading_zero_count = len(target) - len(str(fract_digits))

    sequence.append("pwen")
    sequence.extend(["zewo"] * leading_zero_count)
    sequence += _num_to_text_seq(fract_digits)

    return _finalize(sequence, ordinal=ordinal)


if __name__ == "__main__":  # pragma: no cover
    numbers = [10.4, 0.07, 42, 21, 223, 157, 400_034, 10**6, 10**24 - 1]
    for num in numbers:
        print(num, ":", num_to_text(num, ordinal=False))
