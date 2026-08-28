import re

from kreyolib.convert._vocab import IRREG_ORDINAL_MAP, NUM_TO_TEXT, SCALES, TEXT_TO_NUM

# Scales that ussualy take the prefix `yon`
# When the magnitude is one, e.g., yon milyon.
EXCEPTIONS_SCALES = SCALES - {"san", "mil"}

# Detection regex to detect the first 4 cardinal num
# Since they can also merged with some into some number
FIRST_CARDINALS_DETECTOR = re.compile(r"(?:[yv]?en|de|twa|kat|nèf|[sd]is)$")


def _finalize(text: str, scale_token: str, *, ordinal: bool, fract_digits: int) -> str:
    """Apply ordinal conversion, decimal point, and the yon prefix."""
    if ordinal:
        m = FIRST_CARDINALS_DETECTOR.search(text)
        if m:
            text = text[: m.start()] + IRREG_ORDINAL_MAP[m.group(0)] + text[m.end() :]
        else:
            text += "yèm"
        return text

    if fract_digits:
        text += " pwen " + num_to_text(fract_digits).removeprefix("yon ")

    return "yon " + text if scale_token in EXCEPTIONS_SCALES else text


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

    prefix = "mwens " if input_num < 0 else ""
    input_num = abs(input_num)

    if input_num >= 10**24:
        raise ValueError(f"number too large: maximum supported is 10**24 - 1, got {input_num}")

    # Separate the fraction digits, e.g., 3.14 -> 3 and 14
    parts = str(input_num).split(".")
    input_int = int(parts[0])
    fract_digits = int(parts[1]) if len(parts) > 1 else 0

    # Quick path
    if input_int in NUM_TO_TEXT:
        text = prefix + NUM_TO_TEXT[input_int]
        return _finalize(text, text, ordinal=ordinal, fract_digits=fract_digits)

    sequence = []
    for text, num in TEXT_TO_NUM.items():
        # Prevent ZeroDivisionError
        # It is the end of the map anyway
        if num == 0:
            break

        # Count = magnitude: 0 = nothing
        # e.g., for 42_000, q = 42
        count, input_int = divmod(input_int, num)
        if count == 0:
            pass
        elif count == 1:
            sequence.append(text)
        else:
            sequence.append(f"{num_to_text(count)} {text}")

    text = prefix + " ".join(sequence)
    return _finalize(text, sequence[0], ordinal=ordinal, fract_digits=fract_digits)


if __name__ == "__main__":  # pragma: no cover
    numbers = [10.5, 20, 42, 21, 223, 157, 400_034, 10**6, 10**24 - 1]
    numbers = [10.5]
    for num in numbers:
        print(num, ":", num_to_text(num, ordinal=False))
