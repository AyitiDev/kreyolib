from yasbd import BoundaryDetector

# Initialize the detector and expose the module
_detector = BoundaryDetector(
    "hybridht",
    external_lang_packs=["kreyolib.tokenize._hybrid_ht_rules"],
)


def sent_tokenize(text: str, *, preserve_whitespace: bool = False) -> list[str]:
    """Split text into sentences.

    Args:
        text: The text to tokenize into sentences.
        preserve_whitespace: If ``False`` (default), strip leading and
            trailing whitespace from each sentence.

    Returns:
        A list of sentences.
    """
    return list(_detector.segment(text, preserve_whitespace=preserve_whitespace))


if __name__ == "__main__":  # pragma: no cover
    text = """
    M. Jean te rive maten an. Li te pale ak Me Marie.
    Li di: "Mwen pral vini demen." Apre sa, li ale.
    """

    result = sent_tokenize(text)
    for i, sentence in enumerate(result, 1):
        print(f"{i}: {sentence}")
