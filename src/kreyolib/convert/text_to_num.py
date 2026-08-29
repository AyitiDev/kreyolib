from difflib import SequenceMatcher

from kreyolib.convert._vocab import NUM_TO_TEXT, SCALES, TEXT_TO_NUM

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


def _aggregate_seq(seq: list[int]) -> int:
    """Aggregate number values by applying hierarchical scale multipliers."""
    last_scale = 0
    last_scaled = False
    results = []

    for num in seq:
        text = NUM_TO_TEXT[num]

        if text in SCALES:
            scale = SCALES[text]

            # A lower scale after a scaled value starts a new group.
            if not results or (last_scaled and scale < last_scale):
                results.append(num)

            # A higher scale applies to the entire accumulated value.
            elif scale > last_scale:
                results = [sum(results) * num]

            # An equal scale multiplies the current group.
            else:
                results[-1] *= num

            last_scale = scale
            last_scaled = True
        else:
            results.append(num)
            last_scaled = False

    return sum(results)


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
        int_val = _aggregate_seq(int_seq)
        frac_val = _aggregate_seq(fraq_seq)

        # Positional decimal scaling
        # based on the number of fractional tokens
        # e.g., 5 + (125 / 1000) == 5.125
        leading_zero_count = fraq_seq.count(0)
        fraq_seq_len = leading_zero_count + len(str(frac_val))
        mult_factor = 10**fraq_seq_len
        result = int_val + (frac_val / mult_factor)
    else:
        result = _aggregate_seq(raw_seq)

    return sign * result


def text_to_num(text: str) -> int:
    """Converts Haitian Creole number text into an integer using a left-to-right parser

    Args:
        text: Number written as Haitian Creole words. Minor spelling
            variations may be accepted through fuzzy matching.

    Returns:
        The integer represented by the input text.

    Raises:
        ValueError: Raised if:
            - A token's best fuzzy match does not exceed the
            required confidence threshold.
            - If "mwens" appears other than at the start
            - More than one decimal separator is present
            - consecutive identical word is found
    """
    tokens = text.lower().split()
    sign = 1  # -1 == negative
    is_decimal = False
    prev_word = None
    sequence = []

    # Track integer vs fractional parts for proper decimal scaling
    integer_seq = []

    for i, tok in enumerate(tokens):
        word = _fuzzy_find(tok, i)

        if word == prev_word:
            raise ValueError(f"consecutive identical word is not allowed: {text!r}")

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
            prev_word = None
            continue

        sequence.append(TEXT_TO_NUM[word])
        prev_word = word

    return _finalize(
        sign=sign,
        raw_seq=sequence,
        int_seq=integer_seq,
        is_decimal=is_decimal,
    )


if __name__ == "__main__":  # pragma: no cover
    texts = [
        "mil mil mil",
        "mil san kat",
        "de mil de san",
        "san kat mil",
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
