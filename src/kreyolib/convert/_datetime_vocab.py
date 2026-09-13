WEEKDAYS = [
    "lendi",
    "madi",
    "mèkredi",
    "jedi",
    "vandredi",
    "samdi",
    "dimanch",
]

WEEKDAYS_TO_INDEX = {name: i for i, name in enumerate(WEEKDAYS, start=1)}

MONTHS = [
    "janvye",
    "fevriye",
    "mas",
    "avril",
    "me",
    "jen",
    "jiyè",
    "out",
    "septanm",
    "oktòb",
    "novanm",
    "desanm",
]

MONTHS_TO_INDEX = {name: i for i, name in enumerate(MONTHS, start=1)}

SECONDS_PER_UNIT = {
    "dekad": 10 * 365 * 24 * 60 * 60,
    "ane": 365 * 24 * 60 * 60,
    "mwa": 30 * 24 * 60 * 60,
    "semèn": 7 * 24 * 60 * 60,
    "jou": 24 * 60 * 60,
    "èdtan": 60 * 60,  # More consistent than `è`
    "minit": 60,
    "segonn": 1,
}

UNITS = (
    "segonn",
    "minit",
    "èdtan",
    "jou",
    "semèn",
    "mwa",
    "ane",
    "dekad",
)

UNIT_TRANSLATION = {
    "segonn": "seconds",
    "segond": "seconds",
    "minit": "minutes",
    "è": "hours",
    "zè": "hours",
    "èdtan": "hours",
    "jou": "days",
    "semèn": "weeks",
    "mwa": "months",
    "ane": "years",
    "dekad": "decades",
}

LEXICAL_HOURS = {
    "inè": 1,
    "dezè": 2,
    "twazè": 3,
    "katè": 4,
    "senkè": 5,
    "sizè": 6,
    "setè": 7,
    "uitè": 8,
    "nèvè": 9,
    "dizè": 10,
    "onzè": 11,
    "douzè": 12,
    "trèzè": 13,
    "katòzè": 14,
    "kenzè": 15,
    "sèzè": 16,
    "disetè": 17,
    "dizuitè": 18,
    "diznèvè": 19,
    "ventè": 20,
    "venteyinè": 21,
    "ventedezè": 22,
    "ventetwazè": 23,
    "ventekatrè": 24,
}

DATE_NORMALIZATIONS = {
    # Weekdays
    " len ": " lendi ",
    " mad ": " madi ",
    " mèkr ": " mèkredi ",
    " jed ": " jedi ",
    " vand ": " vandredi ",
    " sam ": " samdi ",
    " dim ": " dimanch ",
    # Months
    " janv ": " janvye ",
    " fevr ": " fevriye ",
    " avr ": " avril ",
    " sept ": " septanm ",
    " okt ": " oktòb ",
    " nov ": " novanm ",
    " des ": " desanm ",
}
