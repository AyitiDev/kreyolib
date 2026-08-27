import pytest

from kreyolib.tokenize.sentence import sent_tokenize
from kreyolib.tokenize.word import word_tokenize


@pytest.mark.parametrize(
    "input_text,expected",
    [
        (
            "Dr. Jean-Louis t'ap travay U.S.A nan Yahoo!",
            ["Dr.", "Jean-Louis", "t", "'", "ap", "travay", "U.S.A", "nan", "Yahoo!"],
        ),
        (
            "Email li a trè senp: Jhon@gmail.com.",
            ["Email", "li", "a", "trè", "senp", ":", "Jhon", "@gmail.com", "."],
        ),
        (
            "@Jhon Sak genla? ##myboy",
            ["@Jhon", "Sak", "genla", "?", "##myboy"],
        ),
        (
            "www.reddit.com popilè anpil ui!",
            ["www.reddit.com", "popilè", "anpil", "ui", "!"],
        ),
    ],
)
def test_word_tokenize(input_text, expected):
    """Test word level tokenization is working smarly."""
    assert word_tokenize(input_text) == expected


@pytest.mark.parametrize(
    "test_case",
    [
        "Alo mond.| Koman ou ye?| Mwen byen.",
        "Gade fig. 2 pou rezilta yo.",
        "M. Dupont est un professeur.",
        "Li te fèt nan mwa janv.| Li te vini an fevriye.",
        "St. Michel se yon kote bèl.| Li toupre vil la.",
        "Chapit 1. Kòmansman an.| Li te fè nwa deyò.",
        "Chapitre 1. Introduction.| Il faisait sombre.",
        "Li te di (Mwen prale demen.) pandan l ap pale.",
        'Li vire bò kote l, "Sa a bèl." li di.',
        'Li di: "Mwen pral vini demen."| Apre sa, li ale.',
        "1.) Premye atik la.| 2.) Dezyèm atik la.",
    ],
)
def test_sentence_tokenize(test_case):
    """Test sentence tokenization is working well."""
    expected = [sent.strip() for sent in test_case.split("|")]
    input_text = test_case.replace("|", "")

    assert sent_tokenize(input_text) == expected
