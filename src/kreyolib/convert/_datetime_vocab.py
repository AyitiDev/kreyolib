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

RElATIVE_DAYS = {
    -2: "avan yè",
    -1: "yè",
    0: "jodi a",
    1: "demèn",
    2: "apre demèn",
}
