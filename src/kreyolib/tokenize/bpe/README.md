# BPE Tokenizer

Byte-Pair Encoding tokenizer for Haitian Creole, built on [SentencePiece](https://github.com/google/sentencepiece). Returns subword tokens, their IDs, and the matching subword embeddings.

## Model provenance

Both files in `data/` come from the [BPEmb project](https://bpemb.h-its.org/ht/), specifically the Haitian Creole (`ht`) model trained on Haitian Creole Wikipedia:

| File | Description |
| --- | --- |
| `ht.wiki.bpe.vs5000.model` | SentencePiece model, 5,000-piece vocabulary |
| `ht.wiki.bpe.vs5000.d100.w2v.bin` | Word2Vec binary, 100 dimensions per token |

## Internals

The embedding dimension is read from the Word2Vec binary's header at load time rather than hardcoded, so retraining at a different width needs no code change.

The loader maps each vector onto its SentencePiece piece ID, allocating a matrix sized to `sp.get_piece_size()` so IDs index rows directly. Tokens present in the binary but absent from the SentencePiece vocabulary would resolve to the same row, so they are skipped to avoid silently overwriting the real `<unk>` vector.

Only the `d100` variants are bundled. To use a different BPEmb configuration, download it from the project page and update the `_MODEL_PATH` / `_BIN_PATH` constants.

## Caching

The processor and the parsed embedding matrix are loaded once per process via `functools.cache` on `_load_bpemb_vectors()`. The first call parses all 5,000 vectors; later calls reuse them. A fresh interpreter re-parses the binary on its first tokenization.

## Empty input

Empty or whitespace-only text short-circuits before the model load and returns a zero-length embedding array of shape `(0, dim)`, so downstream shape checks still hold:

```python
bpe_tokenize("")["embeddings"].shape
# (0, 100)
```
