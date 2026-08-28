from difflib import SequenceMatcher

from kreyolib.convert._vocab import SCALES, TEXT_TO_NUM

# A scale can multiply the preceding value
# while that value is below the scale's next-order boundary
MAX_VALUE_BEFORE_SCALE = 999

# Minimum similarity score for a token to be accepted
# as a valid number word
CONFIDENCE_THRESHOLD = 0.82


def _fuzzy_find(token: str, tok_pos: int) -> str:
    """Finds the vocabulary word most similar to allowed number tokens."""
    score, word = max(
        (
            SequenceMatcher(None, word, token).ratio(),
            word,
        )
        for word in [*list(TEXT_TO_NUM), "mwens", "pwen", "vigil"]
    )

    if score < CONFIDENCE_THRESHOLD:
        raise ValueError(
            f"Unrecognized number word (token num {tok_pos}): "
            f"{token!r} (best match: {word!r}, score: {score:.2f})"
        )
    return word


def _finalize(
    *,
    sign: int | float,
    raw_seq: list,
    int_seq: list,
    is_decimal: bool,
) -> str:
    """Combine int/fraq sequences and applying the sign."""
    if is_decimal:
        fraq_seq = raw_seq
        int_val = sum(int_seq)
        frac_val = sum(fraq_seq)

        # Positional decimal scaling
        # based on the number of fractional tokens
        # e.g., 5 + (125 / 1000) == 5.125
        leading_zero_count = fraq_seq.count(0)
        fraq_seq_len = leading_zero_count + len(str(frac_val))
        mult_factor = 10**fraq_seq_len
        result = int_val + (frac_val / mult_factor)
    else:
        result = sum(raw_seq)

    return sign * result


def text_to_num(text: str) -> int:
    """Converts Haitian Creole number text into an integer using a left-to-right parser

    Args:
        text: Number written as Haitian Creole words. Minor spelling
            variations may be accepted through fuzzy matching.

    Returns:
        The integer represented by the input text.

    Raises:
        ValueError: If a token's best fuzzy match does not exceed the
            required confidence threshold, if "mwens" appears other than
            at the start, or if more than one decimal separator is present.
    """
    tokens = text.lower().split()
    sign = 1  # -1 == negative
    is_decimal = False
    sequence = []

    # Track integer vs fractional parts for proper decimal scaling
    integer_seq = []

    for i, tok in enumerate(tokens):
        word = _fuzzy_find(tok, i)
        if word == "mwens":
            if not i == 0:
                raise ValueError("'mwens' (minus) can only appear at the start of the number")
            sign *= -1
            continue

        if word in {"pwen", "vigil"}:
            if is_decimal:
                raise ValueError(
                    "number text can only contain one decimal separator. "
                    f"Found {word!r} (token num {i})."
                )
            is_decimal = True

            # Move current accumulated items to integer part and switch target
            integer_seq = sequence
            sequence = []
            continue

        num = TEXT_TO_NUM[word]

        if sequence and sequence[-1] < MAX_VALUE_BEFORE_SCALE and word in SCALES:
            sequence[-1] *= num
        else:
            sequence.append(num)

    return _finalize(
        sign=sign,
        raw_seq=sequence,
        int_seq=integer_seq,
        is_decimal=is_decimal,
    )


if __name__ == "__main__":  # pragma: no cover
    texts = [
        "en pwen zewo trannkat",
        "dis vigil senk",
        "mwens de san",
        "de mil san",
        "mil de sann",
        "Krateven disnèf",
        "katreven diznèf",
        "sis san mil katrevan",
        "sen mil kant san senkant senk",
        "mil de san senkannkat",
        "mwens trannde pwen mil de san swasanntuit",
    ]
    for text in texts:
        print(f"{text}:", text_to_num(text))
