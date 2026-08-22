# Kreyolib 🇭🇹

> _Built by haitians for everyone_

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

#### Orthography ([API Reference](https://github.com/AyitiDev/kreyolib/blob/main/API_REFERENCES.md#kreyolibnormalizeorthographystandardize_text))
```python
from kreyolib.normalize.orthography import standardize_text

# Comprehensive cleaning of chat slang, archaic text, clitics, and automatic article correction
messy_text = "Bjr! Mw tap tann ou sou ban a, svp cheri ou knn c fèt mwen jodi a."
standardized_output = standardize_text(messy_text, aggressive=False)
print(standardized_output)  
# Output: Bonjou! Mwen tap tann ou sou ban an, silvouplè cheri ou konn se fèt mwen jodi a.

# Aggressive mode handles older historical variations and non-standard spellings
archaic_text = "Nan lé monn mouin té pèdu nan péché; Min Jézu té sové-m."
modern_output = standardize_text(archaic_text, aggressive=True)
print(modern_output)  
# Output: Nan le mond mwen te pèdi nan peche; Men Jezi te sovem.
```

#### Contractions ([API Reference](https://github.com/AyitiDev/kreyolib/blob/main/API_REFERENCES.md#kreyolibnormalizecontractionsexpand_contractions))
```python
from kreyolib.normalize.contractions import expand_contractions

# Seamlessly expand colloquial clitics into formal standalone tokens across full statements
raw_sentence = "M'ap ale lakay nou paske y'ap tann nou pou n' al travay."
expanded_sentence = expand_contractions(raw_sentence)
print(expanded_sentence)  
# Output: Mwen ap ale lakay nou paske yo ap tann nou pou nou al travay.
```

#### Diacritics ([API Reference](https://github.com/AyitiDev/kreyolib/blob/main/API_REFERENCES.md#kreyolibnormalizediacriticsstrip_diacritics))
```python
from kreyolib.normalize.diacritics import strip_diacritics

# Clean text by removing accent marks for downstream search index normalization or legacy systems
accented_text = "Abèy yo ap vole sou òganizasyon an lè yo ale nan fèt la."
stripped_text = strip_diacritics(accented_text)
print(stripped_text)  
# Output: Abey yo ap vole sou oganizasyon an le yo ale nan fet la.
```

### Advanced Models & Intelligence

#### POS Tagger ([API Reference](https://github.com/AyitiDev/kreyolib/blob/main/API_REFERENCES.md#kreyolibtaggerpostag))
The POS tagger is built on top of Universal Dependencies treebanks and enhanced with custom preprocessing and French-based proper noun handling. For details on training and implementation, see the [Tagger Source Code](https://github.com/AyitiDev/kreyolib/tree/main/src/kreyolib/tagger).

```python
from kreyolib.tagger.pos import tag

# Perform detailed part-of-speech disambiguation on raw string sequences trained using Universal Dependencies treebanks (Autogramm and Adolphe)
sentence_input = "Map vini demen nan maten pou n al travay ansanm."
pos_results = tag(sentence_input)
print(pos_results)  
# Output: [('M', 'PRON'), ('ap', 'AUX'), ('vini', 'VERB'), ('demen', 'NOUN'), ('nan', 'ADP'), ('maten', 'NOUN'), ('pou', 'ADP'), ('n', 'PRON'), ('al', 'VERB'), ('travay', 'VERB'), ('ansanm', 'ADV'), ('.', 'PUNCT')]

# Direct processing utilizing French-based proper noun enhancements and hardcoded copula rules
token_list = ["Mwen", "rele", "Jan", ",", "e", "mwen", "abite", "Okay", "."]
tagged_tokens = tag(token_list)
print(tagged_tokens)
# Output: [('Mwen', 'PRON'), ('rele', 'VERB'), ('Jan', 'PROPN'), (',', 'PUNCT'), ('e', 'CCONJ'), ('mwen', 'PRON'), ('abite', 'VERB'), ('Okay', 'NOUN'), ('.', 'PUNCT')]
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