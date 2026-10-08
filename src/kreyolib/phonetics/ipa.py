import re

from kreyolib.phonetics.syllable import syllabify

# fmt: off
# Basic mapping rules for orthography to IPA
# (tailored for Creole/phonetic consistency)
_IPA_MAPPINGS = {
    # Consonants & Digraphs
    "ch": "ʃ",
    "j": "ʒ",
    "g": "ɡ",
    "ng": "ŋ",
    "w": "w",
    "y": "j",

    # Nasal Vowels / Clusters
    "an": "ã",
    "en": "ẽ",
    "on": "õ",
    "in": "ĩ",

    # Simple Vowels & Accents
    "à": "a",
    "è": "ɛ",
    "ò": "ɔ",
    "e": "e",
    "o": "o",
    "i": "i",
    "u": "u",
    "a": "a",
}
# fmt: on

_SORTED_KEYS = sorted(_IPA_MAPPINGS.keys(), key=len, reverse=True)
_IPA_PATTERN = re.compile(rf"{'|'.join(_SORTED_KEYS)}|\w", re.I)


def _token_to_ipa(token: str) -> str:
    """Converts a single orthographic token or syllable chunk into its IPA equivalent."""

    def replace_match(match):
        val = match.group(0)
        return _IPA_MAPPINGS.get(val, val)

    return _IPA_PATTERN.sub(replace_match, token)


def word_to_ipa(word: str, delimiter: str = ".") -> str:
    """Syllabifies a word and converts it into a syllabified IPA string.

    Args:
        word: The input word.
        delimiter: The character separating syllables in the output (default is '.').

    Returns:
        str: The IPA representation with syllable boundaries.
    """
    word = word.lower()
    syllables = syllabify(word)
    ipa_syllables = [_token_to_ipa(syl) for syl in syllables]
    return delimiter.join(ipa_syllables)


if __name__ == "__main__":  # pragma: no cover
    words = ["achte", "espesyal", "konprann", "anviwonman"]
    for word in words:
        print(f"{word}: {word_to_ipa(word)}")
