<div align="center">
  <img src="https://raw.githubusercontent.com/speedyk-005/kreyolib/main/kreyolib_logo.png" alt="Kreyolib Logo" width="625"/>
  <p><i>"Pa gen ti lang · No language is small"</i></p>
</div>

[![Python Version](https://img.shields.io/badge/Python-3.10%20--%203.14-blue)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/kreyolib?kill_cache=1)](https://pypi.org/project/kreyolib)
[![Coverage Status](https://coveralls.io/repos/github/AyitiDev/kreyolib/badge.svg?branch=main&kill_cache=1)](https://coveralls.io/github/AyitiDev/kreyolib?branch=main)
[![Stability](https://img.shields.io/badge/stability-alpha-yellow)](https://github.com/AyitiDev/kreyolib)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](https://github.com/AyitiDev/kreyolib/actions)
[![lint](https://github.com/AyitiDev/kreyolib/actions/workflows/lint.yml/badge.svg)](https://github.com/AyitiDev/kreyolib/actions/workflows/lint.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/ayitidev/kreyolib/badge)](https://www.codefactor.io/repository/github/ayitidev/kreyolib)
[![License: BSD 3-Clause](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Maintainer](https://img.shields.io/badge/Maintained%20by-AyitiDev-0052B4.svg)](https://github.com/AyitiDev)
[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://badges.frapsoft.com/os/v2/open-source.svg)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> If you like this project, a star ⭐️ would mean a lot :)

---

## Overview / Apèsi

Haitian Creole is spoken by millions of people, but it still lacks many of the language resources and tools available for larger languages. This project aims to build an open-source Ayiti NLP ecosystem focused on creating useful Natural Language Processing tools for Haitian Creole.

Most NLP progress has focused on high-resource languages, while Haitian Creole remains underrepresented. Creating better tools for Haitian Creole can help preserve the language, improve accessibility, and allow more Haitian developers and researchers to build AI applications.

---

## Installation / Enstalasyon

```bash
pip install kreyolib -U
```

---

## Usage / Itilizasyon

### Normalization [API](https://github.com/AyitiDev/kreyolib/blob/main/API_REFERENCES.md#kreyolibnormalize)

#### Orthography ([API](https://github.com/AyitiDev/kreyolib/blob/main/API_REFERENCES.md#kreyolibnormalizeorthographystandardize_text))

Standardizes chat slang, archaic spellings, clitics, and article usage into modern IPN orthography.

```python
from kreyolib.normalize.orthography import standardize_text

# -- Chat slang & abbreviations --
standardize_text("Bjr! Mw tap tann ou sou ban an, svp cheri ou knn c fèt mwen jodi a.")
# Bonjou! Mwen tap tann ou sou ban an, silvouplè cheri ou konn se fèt mwen jodi a.

# -- Article correction --
standardize_text("Mwen chita sou ban a. Mwen ap manje bannann la ki te sou tab lan.")
# Mwen chita sou ban an. Mwen ap manje bannann nan ki te sou tab la.

# -- Capitalization fixes --
standardize_text("mwen renmen bondye")
# Mwen renmen Bondye
```

With `aggressive=True`, older historical variations and non-standard spellings are folded in as well:

```python
standardize_text("Nan lé monn mouin té pèdu nan péché; Min Jézu té sové-m.", aggressive=True)
# Nan le mond mwen te pèdi nan peche; Men Jezi te sovem.
```

#### Contractions ([API](https://github.com/AyitiDev/kreyolib/blob/main/API_REFERENCES.md#kreyolibnormalizecontractionsexpand_contractions))

Expands colloquial clitics (`m'ap`, `y'ap`, `n'`) into formal standalone words.

```python
from kreyolib.normalize.contractions import expand_contractions

expand_contractions("M'ap ale lakay nou paske yap tann nou pou n' al travay.")
# Mwen ap ale lakay nou paske yo ap tann nou pou nou al travay.
```

#### Diacritics ([API](https://github.com/AyitiDev/kreyolib/blob/main/API_REFERENCES.md#kreyolibnormalizediacriticsstrip_diacritics))

Removes accent marks — useful for search indexes or legacy systems that expect plain ASCII.

```python
from kreyolib.normalize.diacritics import strip_diacritics

strip_diacritics("Abèy yo ap vole sou òganizasyon an lè yo ale nan fèt la.")
# Abey yo ap vole sou oganizasyon an le yo ale nan fet la.
```

### Advanced Models & Intelligence

#### POS Tagger ([API](https://github.com/AyitiDev/kreyolib/blob/main/API_REFERENCES.md#kreyolibtaggerpostag))

Built on Universal Dependencies treebanks (Autogramm, Adolphe) with custom preprocessing and French-based proper noun handling. See the [Tagger Source Code](https://github.com/AyitiDev/kreyolib/tree/main/src/kreyolib/tagger) for training details.

Tag a raw sentence:

```python
from kreyolib.tagger.pos import tag

tag("Map vini demen nan maten pou n al travay ansanm.")
# [('M', 'PRON'), ('ap', 'AUX'), ('vini', 'VERB'), ('demen', 'NOUN'), ('nan', 'ADP'),
#  ('maten', 'NOUN'), ('pou', 'ADP'), ('n', 'PRON'), ('al', 'VERB'), ('travay', 'VERB'),
#  ('ansanm', 'ADV'), ('.', 'PUNCT')]
```

Or a pre-tokenized list:

```python
tag(["Mwen", "rele", "Jan", ",", "e", "mwen", "abite", "Okay", "."])
# [('Mwen', 'PRON'), ('rele', 'VERB'), ('Jan', 'PROPN'), (',', 'PUNCT'), ('e', 'CCONJ'),
#  ('mwen', 'PRON'), ('abite', 'VERB'), ('Okay', 'NOUN'), ('.', 'PUNCT')]
```

---

## Roadmap & Progress / Plan Travay

- [ ] **1. Normalization & Preprocessing**
  - [x] Text standardization and modernization
  - [x] Contraction expansion
  - [x] Diacritics remover
  - [ ] Date, number, and text formatters
- [ ] **2. Corpus & Datasets**
  - [x] Stop words and chat/informal abbreviations
  - [ ] Sentences, words, and chat abbreviation maps
  - [ ] Emoji maps with short Kreyòl description values
- [ ] **3. Advanced Models & Intelligence**
  - [x] Part-of-Speech (POS) tagging engine
  - [ ] Named Entity Recognition for Haitian entities
  - [ ] Lexicon-based sentiment analysis engine
  - [ ] Next-word predictor
  - [ ] Regex and rule-based intent matching chatbot
- [ ] **4. Tokenization & Segmentation**
  - [ ] Word tokenizer
  - [ ] Sentence boundary splitter
  - [ ] Social media, tweet, mention, and hashtag tokenization
  - [ ] Subword tokenization via Byte-Pair Encoding and rules
- [ ] **5. Phonetics & Syntax**
  - [ ] Text-to-phonetics and IPA generation
  - [ ] CV syllabification engine
- [ ] **6. Spelling & Error Correction**
  - [ ] Levenshtein distance and spell-checking engine
- [ ] **7. Core Architecture & Pipeline**
  - [ ] Sequential execution pipeline runner

### How People Can Contribute

For ways to contribute, see [Contributing Guide](https://github.com/AyitiDev/kreyolib/blob/main/CONTRIBUTING.md).

> This is a community-driven project to give Haitian Creole a stronger place in the AI and NLP ecosystem.
