# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0] - Unreleased

### Added
- **Sentence Tokenization** ([#3](https://github.com/AyitiDev/kreyolib/pull/271)): Added `sent_tokenize()` to split text into sentences, powered by [yasbd-lib](https://github.com/speedyk-005/yasbd-lib) with Haitian Creole rules extended with French abbreviations and sentence starters.

---

## [0.1.0] - 2026-08-22

Initial release.

### Added
- **Text Standardization & Modernization**: Added rule-based orthography normalization to clean up chat slang, historical variants, and automatic article corrections.
- **Contraction Expansion**: Implemented automatic clitic and contraction expansion to convert conversational forms into full standalone tokens.
- **Diacritics Removal**: Added utility support to strip accent marks for legacy systems and search index normalization.
- **POS Tagging Engine**: Built a specialized Part-of-Speech tagging pipeline trained on Universal Dependencies treebanks (Autogramm and Adolphe).
