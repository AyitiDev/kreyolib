from pathlib import Path

import joblib
from nltk.tokenize import RegexpTokenizer

_MODEL_PATH = Path(__file__).parent / "data" / "pos_tagger.joblib"
_tokenizer = RegexpTokenizer(r"\w+|[^\w\s]")
_model = None

# Sets for contractions that can be split into pronoun + auxiliary
CLITIC_CONTRACTIONS = {"map", "tap", "nap", "wap"}
UNAMBIGUOUS_CONTRACTIONS = {"lap", "yap"}


def _get_model():
    global _model
    if _model is None:
        if not _MODEL_PATH.exists():
            raise FileNotFoundError(
                f"POS tagger model missing at {_MODEL_PATH}. "
                "Ensure package assets are correctly installed."
            )
        _model = joblib.load(_MODEL_PATH)
    return _model


def _preprocess_tokens(tokens: list[str]) -> list[str]:
    """Preprocess tokens to handle noun contexts (like 'yon map') and split contractions."""
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


def tag(inputs: str | list[str]) -> list[tuple[str, str]]:
    """Tag a string or a list of tokens with their respective POS classes.

    Args:
        inputs: Raw text string to be tokenized or an already tokenized list of strings.

    Returns:
        A list of tuples containing each token and its corresponding part-of-speech tag,
            with applicable clitic contractions split.
    """
    if not inputs:
        return []

    tokens = _tokenizer.tokenize(inputs) if isinstance(inputs, str) else inputs
    processed_tokens = _preprocess_tokens(tokens)

    return _get_model().tag(processed_tokens)


if __name__ == "__main__":
    test_sentence = "Lap travay depi lendi. Yon map nan tab la."
    print("String input:", tag(test_sentence))
