from pathlib import Path

import joblib
from nltk.tokenize import RegexpTokenizer

_MODEL_PATH = Path(__file__).parent / "data" / "pos_tagger.joblib"
_FR_NAMES_PATH = Path(__file__).parent / "data" / "firstnames.txt"
_tokenizer = RegexpTokenizer(r"\w+|[^\w\s]")
_model = None
_fr_names = set()

# Sets for contractions that can be split into pronoun + auxiliary
CLITIC_CONTRACTIONS = {"map", "tap", "nap", "wap"}
UNAMBIGUOUS_CONTRACTIONS = {"lap", "yap"}


def _get_model():
    """Load and return the underlying POS tagger model."""
    global _model
    if _model is None:
        _model = joblib.load(_MODEL_PATH)
    return _model


def _get_names_set() -> set:
    """Load the newline-delimited name set into memory if not already loaded.

    Returns:
        A set of lowercase French/foreign first names.
    """
    global _fr_names
    if not _fr_names:
        _fr_names = set(_FR_NAMES_PATH.read_text(encoding="utf-8").splitlines())
    return _fr_names


def _preprocess_tokens(tokens: list[str]) -> list[str]:
    """Preprocess tokens to handle noun contexts and split contractions."""
    processed_tokens = []

    for i in range(len(tokens)):
        current_token = tokens[i]
        current_lower = current_token.lower()

        # Check unambiguous contractions
        if current_lower in UNAMBIGUOUS_CONTRACTIONS:
            # Split a contraction into pronoun + auxiliary marker (e.g., map -> m ap)
            pronoun, aux_marker = current_token[0], current_lower[1:]
            processed_tokens.extend([pronoun, aux_marker])
            continue

        # Check ambiguous contractions
        if current_lower in CLITIC_CONTRACTIONS:
            # If preceded by 'yon', treat as a noun (do not split)
            if i > 0 and tokens[i - 1].lower() == "yon":
                processed_tokens.append(current_token)
                continue

            pronoun, aux_marker = current_token[0], current_lower[1:]
            processed_tokens.extend([pronoun, aux_marker])
            continue

        processed_tokens.append(current_token)

    return processed_tokens


def _postprocess_tokens(tokens: list[str]) -> list[str]:
    """Postprocess tokens to handle French based proper noun and "se" verb."""
    fr_names = _get_names_set()
    processed_tokens = []
    for tok, tag in tokens:
        tok_lower = tok.lower()
        # "se" is always misclassified
        if tok_lower == "se":
            tag = "VERB"
        # Skip tok less longer than 3 to reduce misclassification
        elif len(tok_lower) >= 3 and tok_lower in fr_names:
            tag = "PROPN"

        processed_tokens.append((tok, tag))
    return processed_tokens


def tag(inputs: str | list[str]) -> list[tuple[str, str]]:
    """Tag a string or a list of tokens with their respective POS classes.

    Args:
        inputs: Raw text string to be tokenized or an already tokenized list of strings.

    Returns:
        A list of tuples containing each token and its corresponding part-of-speech tag.
    """
    if not inputs:
        return []

    tokens = _tokenizer.tokenize(inputs) if isinstance(inputs, str) else inputs
    preprocessed_tokens = _preprocess_tokens(tokens)
    return _postprocess_tokens(_get_model().tag(preprocessed_tokens))


if __name__ == "__main__":
    test_sentence = "Map vini demen nan maten."
    test_sentence = ["Li", "se", "Christophe", "."]
    print("Loaded names count:", len(_get_names_set()))
    print("String input:", tag(test_sentence))
