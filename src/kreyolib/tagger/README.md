# Haitian Creole POS Tagger

A specialized Part-of-Speech (POS) tagging pipeline tailored for Haitian Creole, built on top of Universal Dependencies treebanks and enhanced with custom preprocessing and French-based proper noun handling.

## Model Training & Datasets

The underlying model was trained using Haitian Creole treebanks from the **Universal Dependencies** project:

* **[UD_Haitian_Creole-Autogramm](https://github.com/UniversalDependencies/UD_Haitian_Creole-Autogramm)** (Autogramm 3K)
* **[UD_Haitian_Creole-Adolphe](https://github.com/UniversalDependencies/UD_Haitian_Creole-Adolphe)** (Adolphe 71K)

To inspect or clone these datasets locally:
```bash
git clone [https://github.com/UniversalDependencies/UD_Haitian_Creole-Autogramm.git](https://github.com/UniversalDependencies/UD_Haitian_Creole-Autogramm.git)
git clone [https://github.com/UniversalDependencies/UD_Haitian_Creole-Adolphe.git](https://github.com/UniversalDependencies/UD_Haitian_Creole-Adolphe.git)
```
For a detailed side-by-side comparison of these treebanks, check out the [Universal Dependencies Haitian Creole Treebank Comparison](https://universaldependencies.org/treebanks/ht-comparison.html).

---

## Key Features

1. **Clitic Contraction Splitting:** Automatically splits pronoun-auxiliary contractions (such as *lap*, *yap*, *map*, *tap*, *nap*, *wap*) into separate tokens for accurate syntactic analysis, with context-aware handling (e.g., preserving nouns following *yon*).
2. **Proper Noun Enhancement:** Because treebanks primarily contain native Haitian Creole vocabulary, the tagger incorporates a curated list of French-based first names derived from official INSEE data ([eltorio/french_first_names_insee_2024](https://huggingface.co/datasets/eltorio/french_first_names_insee_2024)) to accurately tag personal names as proper nouns (`PROPN`).
3. **Grammatical Rule Corrections:** Hardcodes post-processing rules to fix common statistical model errors, such as always tagging the copula *se* as a `VERB`.

---

## Data Preparation Note

The French first names dataset was originally sourced as a CSV file and processed into a newline-delimited text file (`firstnames.txt`). During preprocessing, entries shorter than 3 characters or those overlapping with common Haitian Creole words were filtered out to prevent false-positive proper noun tags.

## License & Credits

* **Datasets:** Based on the Universal Dependencies Haitian Creole treebanks (Autogramm and Adolphe), licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
* **Contributors:** Claudel Pierre-Louis, Sandra Jagodzińska, Sylvain Kahane, Agata Savary, Emmanuel Schang, and Jephtey Adolphe.
* **Names Dataset:** French first names sourced from INSEE data via [eltorio/french_first_names_insee_2024](https://huggingface.co/datasets/eltorio/french_first_names_insee_2024).
