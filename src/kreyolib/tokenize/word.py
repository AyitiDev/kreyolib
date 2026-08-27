import regex as re
from yasbd.utils.trie import build_optimized_pattern

from kreyolib.tokenize._hybrid_ht_rules import HybridHtRules

ABBREVIATIONS = (
    HybridHtRules.TITLE_ABBRVS
    | HybridHtRules.REFERENCE_ABBRVS
    | HybridHtRules.INLINE_ONLY_ABBRVS
    | HybridHtRules.DATE_ABBRVS
)
EXCLAM_BRANDS = HybridHtRules.NAMES_WITH_EXCLAMATION


# https://regex101.com/r/a8lIq7/3
WORD_TOKENIZER = re.compile(
    rf"""
   (?:https?://|www\.)(?:\.(?!\s)|[^\s\.])+|  # Urls
   (?:\w+[-.]|[#@])+\w+|  # Accronyms/hastags/mentions

   # Preserve abbreviations followed by a dot
   # and brand names with exclamation mark
   {build_optimized_pattern(ABBREVIATIONS)}\.|
   {build_optimized_pattern(EXCLAM_BRANDS)}\!|

   \w+|[^\w\s]     #  Any standalone word or punctuation
   """,
    re.I | re.X,
)


def word_tokenize(text: str) -> list[str]:
    """Split text into word level tokens smartly

    Tokenize text while respecting context for
    hashtags, URLs and emails.

    Args:
        text: The text to tokenize into sentences.

    Returns:
        A list of sentences.
    """
    return WORD_TOKENIZER.findall(text)


if __name__ == "__main__":  # pragma: no cover
    from kreyolib.tokenize.word import word_tokenize

    text = (
        "www.google.com Dr. Jean-Louis t ap travay U.S.A nan Yahoo!"
        " avèk Jhon@gmail.com. ##chill"
    )
    print(word_tokenize(text))
