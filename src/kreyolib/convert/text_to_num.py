from difflib import SequenceMatcher

from kreyolib.convert._vocab import SCALES, TEXT_TO_NUM

# A scale can multiply the preceding value
# while that value is below the scale's next-order boundary
MAX_VALUE_BEFORE_SCALE = 999

# Minimum similarity score for a token to be accepted
# as a valid number word
CONFIDENCE_THRESHOLD = 0.82


def _fuzzy_find(text: str) -> tuple[float, str]:
    """Finds the vocabulary word most similar to NUM_TO_TEXT keys.

    Args:
        text: The text to compare against NUM_TO_TEXT.

    Returns:
        A tuple containing the similarity score and the most similar
        vocabulary word.
    """
    return max(
        (
            SequenceMatcher(None, text, word).ratio(),
            word,
        )
        for word in [*list(TEXT_TO_NUM), "mwens"]
    )


def text_to_num(text: str) -> int:
    """Converts Haitian Creole number text into an integer using a left-to-right parser

    Each token is fuzzy-matched against the known number-word vocabulary.
    A token is accepted only when its similarity score exceeds the
    confidence threshold.

    Args:
        text: Number written as Haitian Creole words. Minor spelling
            variations may be accepted through fuzzy matching.

    Returns:
        The integer represented by the input text.

    Raises:
        ValueError: If a token's best fuzzy match does not exceed the
            required confidence threshold.
    """
    tokens = text.lower().split()
    sign = 1  # -1 == negatige
    sequence = []

    for tok in tokens:
        score, word = _fuzzy_find(tok)

        if score < CONFIDENCE_THRESHOLD:
            raise ValueError(
                f"Unrecognized number word: {tok!r} (best match: {word!r}, score: {score:.2f})"
            )

        if word == "mwens":
            sign *= -1
            continue

        num = TEXT_TO_NUM[word]

        if sequence and sequence[-1] < MAX_VALUE_BEFORE_SCALE and word in SCALES:
            sequence[-1] *= num
        else:
            sequence.append(num)

    return sign * sum(sequence)


if __name__ == "__main__":  # pragma: no cover
    TEXTS = [
        "mwens de san",
        "de mil san",
        "mil de sann",
        "Krateven disnèf",
        "katreven diznèf",
        "sis san mil katrevan",
        "sen mil kant san senkant senk",
        "mil de san senkannkat",
    ]
    for text in TEXTS:
        print(f"{text}:", text_to_num(text))
