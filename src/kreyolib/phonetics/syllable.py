import re

from kreyolib import CONSONANTS

# Tokenize into vowel clusters, common digraphs, or fallback single chars/consonants
_TOKENIZER = re.compile(
    rf"""
	ui|(?:ou|[aeiou])n?|[àèò]|ch|ng|[{"".join(CONSONANTS)}][ywr]|\w
    """,
    re.X | re.I,
)
_VOWEL_PATTERN = re.compile(r"[aeiouàèò]", re.I)


def syllabify(word: str) -> list[str]:
    """Syllabifies a given word into a list of syllable strings using rules.

    Args:
        word: The input word to be syllabified.

    Returns:
        A list containing the segmented syllable chunks.
    """
    tokens = _TOKENIZER.findall(word)
    vowel_indices = [i for i, t in enumerate(tokens) if _VOWEL_PATTERN.match(t)]

    if len(vowel_indices) <= 1:
        return ["".join(tokens)]

    syl_spans = []
    start = 0
    for idx in range(len(vowel_indices) - 1):
        curr_v = vowel_indices[idx]
        next_v = vowel_indices[idx + 1]
        consonants = tokens[curr_v + 1 : next_v]
        c_len = len(consonants)

        # Simple heuristic split: split halfway or give to the next onset
        end = next_v if c_len == 0 else curr_v + 1 + c_len // 2

        syl_spans.append((start, end))
        start = end

    # Final trailing syllable!
    syl_spans.append((start, len(tokens)))

    # Map spans back to text
    return ["".join(tokens[start:end]) for start, end in syl_spans if start < end]


if __name__ == "__main__":  # pragma: no cover
    words = [
        "achte",
        "prepare",
        "ete",
        "espesyal",
        "konprann",
        "bannann",
        "detwi",
        "uit",
        "uitè",
    ]
    for word in words:
        print(f"{word}: {syllabify(word)}")
