from functools import lru_cache
from string import ascii_lowercase

import regex as re

from kreyolib.corpus.chat_abbrvs import CHAT_ABBRVS_MAP

WORD_TOKENIZER = re.compile(r"(?:\w+|[^\w\s])\s*")

# fmt: off
# Automatically derive consonants from the alphabet minus vowels
# (Excluding letters like q, x which aren't standalone in standard Creole,
# but keeping standard alphabet derivation)
_excluding = "aioeuqx"
CONSONANTS = "".join(
    char for char in ascii_lowercase if char not in _excluding
)

# Order matters: Specific/nasal rules must go AFTER general rules
_vowels = "aàeéioòu"
DEFINITE_ARTICLES_FIX_PATTERNS = [
    # Nouns ending in oral vowels take 'a'
    # e.g., mango an -> mango a,
    (re.compile(rf"(?<=[{_vowels}]\b)\s+l?an?\b", re.I), " a"),

    # Nouns ending in oral consonants take 'la'
    # e.g.,  lekòl lan -> lekòl la
    (re.compile(rf"(?<=[{CONSONANTS}]\b)\s+l?an?\b", re.I), " la"),

    # Nouns ending in nasal vowels take 'an'
    # e.g.,  ban a -> ban an
    (re.compile(rf"(?<=[{_vowels}]n\b)\s+l?an?\b", re.I), " an"),

    # Nouns ending in nasal consonants (m, n) take 'nan'/'lan'
    # e.g.,  bannann la -> bannann nan, dam a -> dam lan
    (re.compile(rf"(?<=[{CONSONANTS}][mn]\b)\s+l?a\b", re.I), " nan"),
]

# Manually made map using the chant d'esperans kreyòl context
# I couldn't find them elsewhere
# more aggressive version
OLD_TO_NEW_VOCAB_MAP_1 = {
    # Universal character normalization first
    "é": "e",  # e.g., mérité -> merite
    "-": "",  # e.g., fè-l -> fè l
    "xe": "zye",
    "rai": "ray",
    "ro": "wo",  # e.g., tro -> two
    "ouè": "wè",  # e.g., kouè -> kwè
    "ouin": "wen",  # e.g., mouin -> mwen
    "onn":"ond",  # e.g., monn -> mond
    "oui": "wi",  # e.g., joui -> jwi
    "oue": "we",  # e.g., doue -> dwe
    "uè": "yè", # e.g., Emanuèl -> Emanyèl
    "iè": "yè",  # e.g., priè -> priyè
    "ea": "eya",  # e.g., kréatè -> kreyatè
    "eè": "eyè",  # e.g., Bètleèm-> Bètleyèm
    "agn": "ay",  # e.g., montagn -> montay
    "gn": "y",  # e.g., ansegne -> ansenye
    "oua": "wa",  # e.g., espoua -> espwa
    "ian": "yan",  # e.g., pasian -> pasyans
    "iin": "yen",  # e.g., biin -> byen
    "rò": "wò",  # e.g., ròch -> wòch, tròp -> twòp
    "ie": "ye",  # e.g., krié -> kriye
}

# less aggressive version
OLD_TO_NEW_VOCAB_MAP_2 = {
     # Multi-word phrases
    "koun ye a": "kounye a",
    "la pè": "lapè",

    # Longest specific multi-character sequences
    "bondieu": "Bondye",
    "mouin": "mwen",
    "padonnin": "padone",
    "puisans": "pwisans",
    "puissans": "pwisans",
    "zeprèv": "evrèv",
    "daiti": "dayiti",
    "ouete": "wete",
    "gnou": "yon",
    "roua":"wa",
}

# e.g., du -> di, juska -> jiska
U_WITHOUT_O_OR_I = re.compile(r"(?<![eo])u|u(?=I)", re.I)

# e.g., rinmin -> renmen
IN_WITHOUT_M_OR_N = re.compile(r"(?!m)in|in(?=[mn])", re.I)

# e.g., m'ap -> m ap
CONTRACTIONS_NORM_PATTERN = re.compile(r"([mnwyitk])\s*['’‘]", re.I)
# fmt: on


def _standardize_contractions(text: str) -> str:
    """Standardizes non-standard or variant contractions."""
    return CONTRACTIONS_NORM_PATTERN.sub(r"\1 ", text)


def _expand_chat_abbrvs(word: str) -> str:
    """Expandes chat abbreviations to their full form."""
    was_upper = (word or " ")[0].isupper()

    full_form = CHAT_ABBRVS_MAP.get(word.lower(), word)
    return full_form.capitalize() if was_upper else full_form


def _fix_articles_usage(text: str) -> str:
    """Corrects erroneous usage and formatting surrounding articles."""
    for pat, repl in DEFINITE_ARTICLES_FIX_PATTERNS:
        text = pat.sub(repl, text)
    return text


@lru_cache(maxsize=128)
def _modernize_word(word: str, *, aggressive: bool) -> str:
    """Modernizes a word's orthography."""
    if aggressive:
        # deeper mutations
        for old, new in OLD_TO_NEW_VOCAB_MAP_1.items():
            word = word.replace(old, new)

    word = OLD_TO_NEW_VOCAB_MAP_2.get(word.lower(), word)

    if aggressive:
        word = U_WITHOUT_O_OR_I.sub("i", word)
        word = IN_WITHOUT_M_OR_N.sub("en", word)
    return word


def standardize_text(text: str, *, aggressive: bool = False) -> str:
    """Standardizes input text.

    Applies a series of normalization steps including contraction standardization,
    chat abbreviation expansion, orthography modernization, and article correction
    and more.

    Args:
        text: The input text to process.
        aggressive: Whether to make the deeper but more fragile.
            This is useful if you are parsing really old Haitian creole.
            For example the version in Chant d'esperance Creole'

    Returns:
        The processed text.

    Note:
        Newlines are not preserved; expects a single-paragraph format.
    """
    if not text or text.isspace():
        return ""

    text = _standardize_contractions(text)
    words = WORD_TOKENIZER.findall(text)
    processed_words = []
    for word in words:
        stripped_word = word.rstrip()
        rws = len(word) - len(stripped_word)
        stripped_word = _expand_chat_abbrvs(stripped_word)
        stripped_word = _modernize_word(stripped_word, aggressive=aggressive)
        processed_words.append(stripped_word + (" " * rws))

    processed_text = "".join(processed_words)
    text = _fix_articles_usage(processed_text)

    # Ensure first letter and God names are capitalized
    text = text.replace("jezi", "Jezi").replace("bondye", "Bondye")
    return text[0].upper() + text[1:]


if __name__ == "__main__":  # pragma: no cover
    from kreyolib._debug import print_rich_diff

    TEXT = """
    nan lé monn mouin té pèdu nan péché;
    Min Jézu té sové-m, map rann gloua a li.
    Ak kòd plézi lé monn, mouin té maré,
    Kris té fè-m lib ak puisans li.
    """

    print_rich_diff(TEXT, standardize_text(TEXT, aggressive=True))
