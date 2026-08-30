# fmt: off
ORAL_VOWELS = frozenset({"a", "e", "è", "i", "o", "ò", "ou"})
NASAL_VOWELS = frozenset({"an", "en", "on", "oun", "in"})
CONSONANTS = frozenset({"b", "ch", "d", "f", "g", "h", "j", "k", "l", "m", "n", "ng", "p", "r", "s", "t", "v", "z"})  # noqa: E501
SEMI_VOWELS = frozenset({"w", "y", "ui"})
ALPHABET = ORAL_VOWELS | NASAL_VOWELS | CONSONANTS | SEMI_VOWELS
# fmt: on
