import re

REPLACEMENT_MAP = {
    "é": "e",  # e.g., mérité -> merite
    "iin": "yen",  # e.g., biin -> byen
    "ro": "wo",  # e.g., rouj -> wouj
    "rò": "wò",  # e.g., ròch -> wòch, tròp -> twòp
    "-": "",  # e.g., fè-l -> fè l
    "ie": "ye",  # e.g., vie -> vye
    "oue": "we",  # e.g., ouéte -> wete
    "ouin": "wen",  # e.g., mouin -> mwen
    "oua": "wa",  # e.g., foua -> fwa,
    "ian": "yan",  # e.g., konfian -> konfyan
    "gnou": "yon",
    "du": "di",
    "jezu": "Jezi",
    "bondieu": "Bondye",
    "ape": "ap",  # e.g., pape -> pap, ape -> ap
    "padonnin": "padone",
    "iè": "yè",  # e.g., sièl -> syèl
    "koun ye a": "kounye a",
    "la pè": "lapè",
    "gin": "gen",
}


# e.g., du -> di, juska -> jiska
U_WITHOUT_O_OR_I = re.compile(r"[^o]u|u[^i]", re.I)
