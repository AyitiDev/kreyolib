# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-08-22

Initial release.

### Added
- **Text Standardization & Modernization**: Added rule-based orthography normalization to clean up chat slang, historical variants, and automatic article corrections.
- **Contraction Expansion**: Implemented automatic clitic and contraction expansion to convert conversational forms into full standalone tokens.
- **Diacritics Removal**: Added utility support to strip accent marks for legacy systems and search index normalization.
- **POS Tagging Engine**: Built a specialized Part-of-Speech tagging pipeline trained on Universal Dependencies treebanks (Autogramm and Adolphe).
- **Proper Noun Enhancement**: Integrated a curated French-first-names dataset from INSEE data to accurately tag personal names as proper nouns (`PROPN`).
- **Grammatical Rule Overrides**: Added post-processing rules to enforce strict handling of core terms like the copula *se*.
