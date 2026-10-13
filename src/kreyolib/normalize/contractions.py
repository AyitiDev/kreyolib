import regex as re

# https://regex101.com/r/sH3MjG/13
# First branch: clitic + (space or a following auxiliary/verb).
# Second branch: fused future forms (ma, na, wa, ya) where the clitic
# is directly joined to the future marker "a".
CONTRACTIONS_FINDER = re.compile(
    r"""
    (?<!(?:pral|yon|se|te|ape?)\s+)\b
    (?:
        ((?:mt|[mtnwyikl])\s*(?:['’‘,;:.!?])?)\s*
        (?:(?<=\s)|$|(?=(?:pral|al|ap)e?|ta))
        |
        ([mnwy])(?=a\b(?!\s*a\b))
    )
    """,
    re.I | re.X,
)

CONTRACTIONS_MAP = {
    "mt": "mwen te",
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
        matched = (match.group(1) or match.group(2)).strip()
        last_char = matched[-1]
        cleaned_matched = "".join([c for c in matched if c.isalpha()])
        was_upper = matched[0].isupper()

        full_form = CONTRACTIONS_MAP.get(cleaned_matched.lower(), cleaned_matched)
        full_form += last_char + " " if last_char in ",;:.!?" else " "
        return full_form.capitalize() if was_upper else full_form

    return CONTRACTIONS_FINDER.sub(replace, text)


if __name__ == "__main__":  # pragma: no cover
    from kreyolib._debug import print_rich_diff

    text = "l. M' ap ale demen. Mtap di ou l'ap vini jodya. Na pale pita. Al prepare l:"
    print_rich_diff(text, expand_contractions(text))
