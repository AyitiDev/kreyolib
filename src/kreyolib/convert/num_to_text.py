import re

from kreyolib.convert._vocab import NUM_TO_TEXT, SCALES, TEXT_TO_NUM

# Scales that ussualy take the prefix `yon`
# When the magnitude is one, e.g., yon milyon.
EXCEPTIONS_SCALES = SCALES - {"san", "mil"}

IRREGULAR_ORDINAL_MAP = {
    "en": "premye",
    "de": "dezyèm",
    "twa": "twazyèm",
    "kat": "katriyèm",
    "sis": "sizyèm",
    "nèf": "nevyèm",
    "dis": "dizyèm",
    "ven": "ventyèm",
    "yen": "yinyèm",
}

# Detection regex to detect the first 4 cardinal num
# Since they can also merged with some into some number
FIRST_CARDINALS_DETECTOR = re.compile(r"(?:[yv]?en|de|twa|kat|nèf|[sd]is)$")


def _convert_to_ordinal(text: str) -> str:
    """Convert a numerical text to its ordinal form."""
    m = FIRST_CARDINALS_DETECTOR.search(text)

    if m:
        text = text[: m.start()] + IRREGULAR_ORDINAL_MAP[m.group(0)] + text[m.end() :]
    else:
        text += "yèm"

    return text


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
    if ordinal and input_num < 1:
        raise ValueError("ordinal form requires a number that is greater than zero")

    prefix = "mwens " if input_num < 0 else ""
    input_num = abs(input_num)

    if input_num >= 10**24:
        raise ValueError(f"number too large: maximum supported is 10**24 - 1, got {input_num}")

    # Quick path
    if input_num in NUM_TO_TEXT:
        text = prefix + NUM_TO_TEXT[input_num]
        if ordinal:
            return _convert_to_ordinal(text)
        return "yon " + text if text in EXCEPTIONS_SCALES else text

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

    text = prefix + " ".join(sequence)

    if ordinal:
        return _convert_to_ordinal(text)
    return "yon " + text if sequence[0] in EXCEPTIONS_SCALES else text


if __name__ == "__main__":  # pragma: no cover
    numbers = [10, 20, 42, 21, 223, 157, 400_034, 10**6, 10**24 - 1]
    for num in numbers:
        print(num, ":", num_to_text(num, ordinal=True))
