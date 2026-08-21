import regex as re

# https://regex101.com/r/sH3MjG/7
CONTRACTIONS_FINDER = re.compile(
    r"""
    (?<!yon\s+)\b([mtnwyikl])(?:\s*['’‘])?
    (?:\s+|(?=(?:(pral|al|ap)e?|ta)\b))
    """,
    re.I | re.X,
)

CONTRACTIONS_MAP = {"m": "mwen", "t": "te", "l": "li", "n": "nou", "y": "yo"}


def expand_contractions(text: str) -> str:
    """Expands short clitics or contractions found in the text

    Args:
        text: The input string containing clitics/contractions.

    Returns:
        The text with contractions expanded to full words.
    """

    def replace(match: re.Match) -> str:
        # Extract the matched clitic character
        matched_char = match.group(1)
        print(matched_char)
        was_upper = matched_char.isupper()

        full_form = CONTRACTIONS_MAP.get(matched_char.lower(), match.group(1)) + " "
        return full_form.title() if was_upper else full_form

    return CONTRACTIONS_FINDER.sub(replace, text)


if __name__ == "__main__":  # pragma: no cover
    from kreyolib._debug import print_rich_diff

    text = "M'ap ale demen. M tap di ou l'ap vini jodya."
    print_rich_diff(text, expand_contractions(text))
