import regex as re

# https://regex101.com/r/sH3MjG/10
# First branch: clitic + (space or a following auxiliary/verb).
# Second branch: fused future forms (ma, na, wa, ya) where the clitic
# is directly joined to the future marker "a".
CONTRACTIONS_FINDER = re.compile(
    r"""
    (?<!(?:pral|yon|se|te|ape?)\s+)\b
    (?:
        ([mtnwyikl](?:\s*['’‘])?)\s*
        (?:(?<=\s)|(?=(?:pral|al|ap)e?|ta))
        |
        ([mnwy])(?=a\b(?!\s*a\b))
    )
    """,
    re.I | re.X,
)

CONTRACTIONS_MAP = {
    "m": "mwen",
    "t": "te",
    "l": "li",
    "n": "nou",
    "y": "yo",
    "w": "ou",
}


def expand_contractions(text: str) -> str:
    """Expands short clitics or contractions found in the text

    Args:
        text: The input string containing clitics/contractions.

    Returns:
        The text with contractions expanded to full words.
    """

    def replace(match: re.Match) -> str:
        # Extract the matched clitic character (group 1 or the fused form in group 2)
        first_ch = (match.group(1) or match.group(2))[0]
        was_upper = first_ch.isupper()

        full_form = CONTRACTIONS_MAP.get(first_ch.lower(), first_ch) + " "
        return full_form.capitalize() if was_upper else full_form

    return CONTRACTIONS_FINDER.sub(replace, text)


if __name__ == "__main__":  # pragma: no cover
    from kreyolib._debug import print_rich_diff

    text = "M' ap ale demen. M tap di ou l'ap vini jodya. Na pale pita. Wa a fache."
    print_rich_diff(text, expand_contractions(text))
