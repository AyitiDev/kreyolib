<div align="center">
  <img src="https://raw.githubusercontent.com/AyitiDev/kreyolib/main/kreyolib_logo.png" alt="Kreyolib Logo" width="625"/>
  <p><i>"Kreyòl merite zouti tou · Kreyòl deserves tools too"</i></p>
</div>

[![Python Version](https://img.shields.io/badge/Python-3.10%20--%203.14-blue)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/kreyolib?kill_cache=1)](https://pypi.org/project/kreyolib)
[![Coverage Status](https://coveralls.io/repos/github/AyitiDev/kreyolib/badge.svg?branch=main&kill_cache=1)](https://coveralls.io/github/AyitiDev/kreyolib?branch=main)
[![Stability](https://img.shields.io/badge/stability-alpha-red)](https://github.com/AyitiDev/kreyolib)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](https://github.com/AyitiDev/kreyolib/actions)
[![lint](https://github.com/AyitiDev/kreyolib/actions/workflows/lint.yml/badge.svg)](https://github.com/AyitiDev/kreyolib/actions/workflows/lint.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/ayitidev/kreyolib/badge)](https://www.codefactor.io/repository/github/ayitidev/kreyolib)
[![License: BSD 3-Clause](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Maintainer](https://img.shields.io/badge/Maintained%20by-AyitiDev-0052B4.svg)](https://github.com/AyitiDev)
[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://badges.frapsoft.com/os/v2/open-source.svg)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> If you like this project, a star ⭐️ would mean a lot :)

---

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Overview / Apèsi](#overview--ap%C3%A8si)
- [Installation / Enstalasyon](#installation--enstalasyon)
- [Usage / Itilizasyon](#usage--itilizasyon)
  - [Alphabet / Alfabèt](#alphabet--alfab%C3%A8t)
  - [Normalization](#normalization)
    - [Orthography (API)](#orthography-api)
    - [Contractions (API)](#contractions-api)
    - [Diacritics (API)](#diacritics-api)
  - [Tokenization](#tokenization)
    - [Sentence Splitter (API)](#sentence-splitter-api)
    - [Word Tokenizer (API)](#word-tokenizer-api)
  - [Conversion](#conversion)
    - [Number to Text (API)](#number-to-text-api)
    - [Text to Number (API)](#text-to-number-api)
    - [Datetime to Text (API)](#datetime-to-text-api)
    - [Text to Datetime (API)](#text-to-datetime-api)
  - [Advanced Models & Intelligence](#advanced-models--intelligence)
    - [POS Tagger (API)](#pos-tagger-api)
- [Roadmap & Progress / Plan Travay](#roadmap--progress--plan-travay)
  - [How People Can Contribute](#how-people-can-contribute)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

---

## Overview / Apèsi

Haitian Creole is spoken by millions of people, but it still lacks many of the language resources and tools available for larger languages. This project aims to build an open-source Ayiti NLP ecosystem focused on creating useful Natural Language Processing tools for Haitian Creole.

Most NLP progress has focused on high-resource languages, while Haitian Creole remains underrepresented. Creating better tools for Haitian Creole can help preserve the language, improve accessibility, and allow more Haitian developers and researchers to build AI applications.

---

## Installation / Enstalasyon

```bash
pip install kreyolib -U

# If you are going to do text_to _datetime
pip install kreyolib[datetime] -U
```

---

## Usage / Itilizasyon

### Alphabet / Alfabèt

The package exposes the full Haitian Creole alphabet as frozen sets for phonology and tokenization work:

```python
from kreyolib import (
    ORAL_VOWELS,
    NASAL_VOWELS,
    CONSONANTS,
    SEMI_VOWELS,
    ALPHABET,
)

ORAL_VOWELS  # frozenset({'a', 'e', 'è', 'i', 'o', 'ò', 'ou'})
NASAL_VOWELS  # frozenset({'an', 'en', 'on', 'oun', 'in'})
CONSONANTS  # frozenset({'b', 'ch', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'ng', 'p', 'r', 's', 't', 'v', 'z'})
SEMI_VOWELS  # frozenset({'w', 'y', 'ui'})
ALPHABET  # Combines all
```

### Normalization

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

### Tokenization

#### Sentence Splitter ([API](https://github.com/AyitiDev/kreyolib/blob/main/API_REFERENCES.md#kreyolibtokenizesentencesent_tokenize))

Splits text into sentences, respecting abbreviations, quotes, and parenthesized boundaries. Powered by [yasbd-lib](https://github.com/speedyk-005/yasbd-lib/blob/main/src/yasbd/rules/__init__.py), with Haitian Creole rules extended with French abbreviations and sentence starters.

```python
from kreyolib.tokenize.sentence import sent_tokenize

sent_tokenize("Alo mond. Koman ou ye? Mwen byen.")
# ['Alo mond.', 'Koman ou ye?', 'Mwen byen.']

sent_tokenize(
    'M. Dupont est un professeur. Li travay nan lekòl la. Li di: "Mwen pral vini demen." Apre sa, li ale.'
)
# ['M. Dupont est un professeur.', 'Li travay nan lekòl la.', 'Li di: "Mwen pral vini demen."', 'Apre sa, li ale.']
```

#### Word Tokenizer ([API](https://github.com/AyitiDev/kreyolib/blob/main/API_REFERENCES.md#kreyolibtokenizewordword_tokenize))

Splits text into word-level tokens while preserving abbreviations, hashtags, mentions, and URLs.

```python
from kreyolib.tokenize.word import word_tokenize

word_tokenize("Dr. Jean-Louis t'ap travay U.S.A nan Yahoo!")
# ['Dr.', 'Jean-Louis', 't', "'", 'ap', 'travay', 'U.S.A', 'nan', 'Yahoo!']

word_tokenize("@Jhon Sak genla? ##myboy")
# ['@Jhon', 'Sak', 'genla', '?', '##myboy']

word_tokenize("www.google.com avèk Jhon@gmail.com.")
# ['www.google.com', 'avèk', 'Jhon', '@gmail.com', '.']
```

### Conversion

#### Number to Text ([API](https://github.com/AyitiDev/kreyolib/blob/main/API_REFERENCES.md#kreyolibconvertnum_to_textnum_to_text))

Converts an integer or decimal into its Kreyòl word form. It also supports negative numbers and ordinal numbers.

```python
from kreyolib.convert.num_to_text import num_to_text

print(num_to_text(223))  # 'de san venntwa'
print(num_to_text(1_000_000))  # 'yon milyon'
print(num_to_text(12.4))  # 'douz pwen kat'
print(num_to_text(-5))  # 'mwens senk'
print(num_to_text(400_034))  # 'kat san mil trannkat'
print(num_to_text(0.17))  # 'zewo pwen disèt'
print(num_to_text(0.014))  # 'zewo pwen zewo katòz'
print(num_to_text(42, ordinal=True))  # 'san vennkatryèm'
print(num_to_text(124, ordinal=True))  # 'karanndezyèm'
```

#### Text to Number ([API](https://github.com/AyitiDev/kreyolib/blob/main/API_REFERENCES.md#kreyolibconverttext_to_numtext_to_num))

Converts Kreyòl number words back into an integer or float. The converter supports negative numbers and decimals and tolerates minor spelling variations through fuzzy matching.

```python
from kreyolib.convert.text_to_num import text_to_num

print(text_to_num("de san venntwa"))  # 223
print(text_to_num("yon milyon san uit"))  # 1000008
print(text_to_num("douz pwen kat"))  # 12.4
print(text_to_num("mwens de san"))  # -200
print(text_to_num("de mil de san"))  # 200200
print(text_to_num("de san de mil"))  # 202000
print(text_to_num("zewo pwen zewo uit"))  # 0.08
print(text_to_num("kat milyon de san karanntwa"))  # 4_000_243
```

#### Datetime to Text ([API](https://github.com/AyitiDev/kreyolib/blob/main/API_REFERENCES.md#kreyolibconvertdatetime_to_textdatetime_to_text))

Converts a `datetime` or `timedelta` into Kreyòl date, time, or relative-time text.

> [!NOTE]
> Relative datetime outputs depend on the current time, so results may vary depending on when the function is called.
> These were run with datetime(2026, 1, 1) reference

```python
from datetime import datetime, timedelta

from kreyolib.convert.datetime_to_text import datetime_to_text

print(datetime_to_text(datetime(2026, 9, 4)))
# 'vandredi 4 septanm 2026'

print(datetime_to_text(datetime(2023, 12, 3, 15, 30, 42)))
# 'dimanch 3 desanm 2023, 15:30:42'

print(datetime_to_text(-timedelta(weeks=4, days=8), relative=True))
# 'sa gen 1 mwa e 5 jou'

print(datetime_to_text(timedelta(weeks=12, days=3, hours=60), relative=True))
# 'nan 2 mwa, 4 semèn e 12 èdtan'
```

Relative conversion can express a duration from the current time.

```python
print(datetime_to_text(timedelta(hours=5), relative=True))
# 'jodi a, nan 5 èdtan'
```

#### Text to Datetime ([API](https://github.com/AyitiDev/kreyolib/blob/main/API_REFERENCES.md#kreyolibconverttext_to_datetimetext_to_datetime))

Parses Kreyòl date and time expressions into a `datetime` object. It supports numeric timestamps, absolute dates, relative dates, relative durations, weekdays, periods, and common time expressions.

> [!NOTE]
> Relative expressions are resolved against the current time, so their resulting `datetime` may vary depending on when the function is called.
> Those were ran against datetime(2026, 1, 1) reference.

```python
from kreyolib.convert.text_to_datetime import text_to_datetime

print(text_to_datetime("2026-01-08 22:33"))
# datetime(2026, 1, 8, 22, 33)

print(text_to_datetime("samdi 1 janvye 2019"))
# datetime(2019, 1, 1)

print(text_to_datetime("demen"))
# datetime(2026, 1, 2)

print(text_to_datetime("semèn pwochèn a 10h"))
# datetime(2026, 1, 8, 10, 0)

print(text_to_datetime("demen a dizè"))
# datetime(2026, 1, 2, 10, 0)
```

Relative expressions can describe durations, previous or upcoming periods, and weekdays.

```python
print(text_to_datetime("sa gen yon ane"))
# datetime(2025, 1, 1)

print(text_to_datetime("sa gen 5 jou, kat semèn"))
# datetime(2025, 11, 29)

print(text_to_datetime("semèn pase"))
# datetime(2025, 12, 25)

print(text_to_datetime("madi pase"))
# datetime(2025, 12, 31)

print(text_to_datetime("mwa kap vini a"))
# datetime(2026, 2, 1)
```

Time expressions can be combined with relative or absolute date expressions.

```python
print(text_to_datetime("avan yè a 10:45"))
# datetime(2025, 12, 30, 10, 45)

print(text_to_datetime("apre demen a 15è eka"))
# datetime(2026, 1, 3, 15, 15)

print(text_to_datetime("jedi pase a 3è edmi"))
# datetime(2025, 12, 26, 3, 30)

print(text_to_datetime("jedi pwochèn"))
# datetime(2026, 1, 8)
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

- [x] **1. Normalization & Preprocessing**
  - [x] Text standardization and modernization
  - [x] Contraction expansion
  - [x] Diacritics remover
- [x] **2. Conversion**
  - [x] Number-to-text conversion in Kreyòl with bidirectional support
  - [x] Datetime-to-text conversion in Kreyòl with bidirectional support
- [ ] **3. Corpus & Datasets**
  - [x] Stop words
  - [x] Chat/informal abbreviations
  - [ ] Sentences and words
- [ ] **4. Advanced Models & Intelligence**
  - [x] Part-of-Speech (POS) tagging engine (ml)
  - [ ] Named Entity Recognition for Haitian entities (ml)
  - [ ] Lexicon-based sentiment analysis engine
  - [ ] Sentence/Next-word predictor
- [ ] **5. Tokenization & Segmentation**
  - [x] Context-aware Word tokenizer
  - [x] Sentence boundary splitter (with support for mention, and hashtag)
  - [ ] Subword tokenization via Byte-Pair Encoding and rules
- [ ] **6. Phonetics & Syntax**
  - [ ] Text-to-phonetics and IPA generation
  - [ ] CV syllabification engine
- [ ] **7. Spelling & Error Correction**
  - [ ] Spell-checking engine
- [ ] **8. Core Architecture & Pipeline**
  - [ ] Sequential execution pipeline runner

### How People Can Contribute

For ways to contribute, see [Contributing Guide](https://github.com/AyitiDev/kreyolib/blob/main/CONTRIBUTING.md).

> This is a community-driven project to give Haitian Creole a stronger place in the AI and NLP ecosystem.
