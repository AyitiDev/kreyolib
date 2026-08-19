import unicodedata


def strip_diacritics(text: str) -> str:
    """Removes diacritic marks entirely (è -> e, ò -> o).

    Args:
        text: The input text

    Returns: A text without the diacritic marks
    """
    if not text or text.isspace():
        return text

    nfd_form = unicodedata.normalize("NFD", text)

    # Filter out characters whose category starts with 'M'
    # (Mark / combining diacritics)
    return "".join(c for c in nfd_form if not unicodedata.category(c).startswith("M"))


if __name__ == "__main__":  # pragma: no cover
    from kreyolib._debug import print_rich_diff

    text = "Kilè ou te fè sa?"
    cleaned_text = strip_diacritics(text)
    print_rich_diff(text, cleaned_text)
