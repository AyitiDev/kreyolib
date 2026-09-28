from functools import cache
from pathlib import Path
from typing import Any, BinaryIO

import numpy as np
import sentencepiece as spm

_MODEL_PATH = Path(__file__).parent / "data" / "ht.wiki.bpe.vs5000.model"
_BIN_PATH = Path(__file__).parent / "data" / "ht.wiki.bpe.vs5000.d100.w2v.bin"


def _read_token_label(f: BinaryIO) -> str:
    """Reads and decodes the UTF-8 token label from a Word2Vec binary stream.

    Word2Vec binary format separates string labels from raw float vectors
    with a single space byte (0x20).
    """
    word_bytes = bytearray()
    while True:
        ch = f.read(1)
        if ch in {b" ", b""}:
            break
        word_bytes.extend(ch)
    return word_bytes.decode("utf-8")


@cache
def _load_bpemb_vectors() -> tuple[spm.SentencePieceProcessor, np.ndarray]:
    """Loads SentencePiece processor and parses Word2Vec binary embeddings.

    Returns:
        A tuple containing:
            - spm.SentencePieceProcessor: Initialized SentencePiece processor.
            - np.ndarray: Float32 embedding matrix indexed by subword ID.

    Raises:
        FileNotFoundError: If either MODEL_PATH or BIN_PATH does not exist.
        ValueError: If the Word2Vec header format is invalid.
    """
    sp = spm.SentencePieceProcessor()
    sp.load(str(_MODEL_PATH))

    with _BIN_PATH.open("rb") as f:
        header = f.readline().decode("utf-8").strip()
        try:
            vocab_size, dim = map(int, header.split())
        except ValueError as err:
            raise ValueError(f"Invalid Word2Vec binary header: '{header}'") from err

        # Match full SentencePiece vocab size so IDs map directly to row indices
        vectors = np.zeros((sp.get_piece_size(), dim), dtype=np.float32)

        for _ in range(vocab_size):
            word = _read_token_label(f)

            # Word2Vec binary stores float32 values contiguously (4 bytes per float)
            vector_data = f.read(dim * 4)
            vector = np.frombuffer(vector_data, dtype=np.float32)

            sp_id = sp.piece_to_id(word)

            # Prevent unmapped binary tokens from silently overwriting the actual UNK vector
            if sp_id != sp.unk_id() or word == sp.id_to_piece(sp.unk_id()):
                vectors[sp_id] = vector

    return sp, vectors


def bpe_tokenize(text: str, *, lowercase: bool = True) -> dict[str, Any]:
    """Tokenizes input text and retrieves corresponding subword embeddings.

    Args:
        text: Input string to tokenize.
        lowercase: Whether to convert text to lowercase before tokenization.
            Defaults to True.

    Returns:
        A dictionary containing:
            - "tokens": List of subword string tokens.
            - "ids": List of integer token IDs.
            - "embeddings": Array of shape `(seq_len, dim)` containing
              subword embeddings.
    """
    if not text or text.isspace():
        return {
            "tokens": [],
            "ids": [],
            "embeddings": np.ndarray([], dtype=np.float32),
        }

    processed_text = text.lower() if lowercase else text
    sp, vectors = _load_bpemb_vectors()

    tokens = sp.encode_as_pieces(processed_text)
    token_ids = sp.encode_as_ids(processed_text)

    # Fast O(1) row lookup avoiding manual loops over individual sequence tokens
    embeddings = vectors[token_ids]

    return {
        "tokens": tokens,
        "ids": token_ids,
        "embeddings": embeddings,
    }


if __name__ == "__main__":  # pragma: no cover
    result = bpe_tokenize(
        "Kreyòl ayisyen se yon bèl lang. kreyòl ayisyen se dezyèm lang ki pale nan kiba."
    )

    print("Tokens:", result["tokens"])
    print("IDs:", result["ids"])
    print("Shape:", result["embeddings"].shape)
