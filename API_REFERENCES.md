# Table of Contents

* [kreyolib.corpus.chat\_abbrvs](#kreyolib.corpus.chat_abbrvs)
* [kreyolib.corpus](#kreyolib.corpus)
* [kreyolib.corpus.stop\_words](#kreyolib.corpus.stop_words)
* [kreyolib.\_debug](#kreyolib._debug)
  * [print\_rich\_diff](#kreyolib._debug.print_rich_diff)
* [kreyolib](#kreyolib)
* [kreyolib.normalize.contractions](#kreyolib.normalize.contractions)
  * [expand\_contractions](#kreyolib.normalize.contractions.expand_contractions)
* [kreyolib.normalize.diacritics](#kreyolib.normalize.diacritics)
  * [strip\_diacritics](#kreyolib.normalize.diacritics.strip_diacritics)
* [kreyolib.normalize](#kreyolib.normalize)
* [kreyolib.normalize.orthography](#kreyolib.normalize.orthography)
  * [standardize\_text](#kreyolib.normalize.orthography.standardize_text)
* [kreyolib.tagger](#kreyolib.tagger)
* [kreyolib.tagger.pos](#kreyolib.tagger.pos)
  * [tag](#kreyolib.tagger.pos.tag)
* [kreyolib.tokenize.\_hybrid\_ht\_rules](#kreyolib.tokenize._hybrid_ht_rules)
  * [HybridHtRules](#kreyolib.tokenize._hybrid_ht_rules.HybridHtRules)
* [kreyolib.tokenize](#kreyolib.tokenize)
* [kreyolib.tokenize.sentence](#kreyolib.tokenize.sentence)
  * [sent\_tokenize](#kreyolib.tokenize.sentence.sent_tokenize)

<a id="kreyolib.corpus.chat_abbrvs"></a>

# kreyolib.corpus.chat\_abbrvs

<a id="kreyolib.corpus"></a>

# kreyolib.corpus

<a id="kreyolib.corpus.stop_words"></a>

# kreyolib.corpus.stop\_words

<a id="kreyolib._debug"></a>

# kreyolib.\_debug

<a id="kreyolib._debug.print_rich_diff"></a>

#### print\_rich\_diff

```python
def print_rich_diff(text1: str, text2: str) -> None
```

Renders a colorized diff of two strings using ANSI escape codes.

<a id="kreyolib"></a>

# kreyolib

<a id="kreyolib.normalize.contractions"></a>

# kreyolib.normalize.contractions

<a id="kreyolib.normalize.contractions.expand_contractions"></a>

#### expand\_contractions

```python
def expand_contractions(text: str) -> str
```

Expands short clitics or contractions found in the text

**Arguments**:

- `text` - The input string containing clitics/contractions.
  

**Returns**:

  The text with contractions expanded to full words.

<a id="kreyolib.normalize.diacritics"></a>

# kreyolib.normalize.diacritics

<a id="kreyolib.normalize.diacritics.strip_diacritics"></a>

#### strip\_diacritics

```python
def strip_diacritics(text: str) -> str
```

Removes diacritic marks entirely (è -> e, ò -> o).

<a id="kreyolib.normalize"></a>

# kreyolib.normalize

<a id="kreyolib.normalize.orthography"></a>

# kreyolib.normalize.orthography

<a id="kreyolib.normalize.orthography.standardize_text"></a>

#### standardize\_text

```python
def standardize_text(text: str, *, aggressive: bool = False) -> str
```

Standardizes input text.

Applies a series of normalization steps including fix mojibakes,
contraction standardization, chat abbreviation expansion,
orthography modernization, and article correction and more.

**Arguments**:

- `text` - The input text to process.
- `aggressive` - Whether to make the deeper but more fragile.
  This is useful if you are parsing really old Haitian creole.
  For example the version in Chant d'esperance Creole'
  

**Returns**:

  The processed text.
  

**Notes**:

  Newlines are not preserved; expects a single-paragraph format.

<a id="kreyolib.tagger"></a>

# kreyolib.tagger

<a id="kreyolib.tagger.pos"></a>

# kreyolib.tagger.pos

<a id="kreyolib.tagger.pos.tag"></a>

#### tag

```python
def tag(inputs: str | list[str]) -> list[tuple[str, str]]
```

Tag a string or a list of tokens with their respective POS classes.

**Arguments**:

- `inputs` - Raw text string to be tokenized or an already tokenized list of strings.
  

**Returns**:

  A list of tuples containing each token and its corresponding part-of-speech tag.

<a id="kreyolib.tokenize._hybrid_ht_rules"></a>

# kreyolib.tokenize.\_hybrid\_ht\_rules

<a id="kreyolib.tokenize._hybrid_ht_rules.HybridHtRules"></a>

## HybridHtRules Objects

```python
class HybridHtRules(HtRules)
```

Extend the base Haitian rules with some French awareness abbreviations.

<a id="kreyolib.tokenize"></a>

# kreyolib.tokenize

<a id="kreyolib.tokenize.sentence"></a>

# kreyolib.tokenize.sentence

<a id="kreyolib.tokenize.sentence.sent_tokenize"></a>

#### sent\_tokenize

```python
def sent_tokenize(text: str,
                  *,
                  preserve_whitespace: bool = False) -> list[str]
```

Split text into sentences.

**Arguments**:

- `text` - The text to tokenize into sentences.
- `preserve_whitespace` - If ``False`` (default), strip leading and
  trailing whitespace from each sentence.
  

**Returns**:

  A list of sentences.

