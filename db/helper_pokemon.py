import re


def helper_pokemon_get_number(entry):
    patterns_list = [
            "^(\d+)$",       # 78, 79
            "^(\d+)[a-z]$",  # 78a, 78b
            "^[a-zA-Z](\d+)$"       # H78, H79
        ]

    number = None
    for pattern in patterns_list:
        matches = re.match(pattern, entry.number)
        if matches is None:
            continue

        number = matches.group(1)
        break

    return int(number)


def helper_pokemon_get_sub_number(entry):
    patterns_list = [
        "^\d+([a-z])$",  # 78a, 78b
        "^([a-zA-Z])\d+$"  # H78, H79
    ]

    sub_number = None
    for pattern in patterns_list:
        matches = re.match(pattern, entry.number)
        if matches is None:
            continue

        sub_number = matches.group(1)
        break

    return sub_number


def helper_pokemon_get_name(entry):
    patterns_list = [
        "(.*)\s\([0-9]*\)",  # toto (70)
        "^(.*)\s\([0-9]*.+\)"  # toto (70a)
    ]

    name = entry.name
    for pattern in patterns_list:
        matches = re.match(pattern, entry.name)
        if matches is None:
            continue

        name = matches.group(1)
        break

    return name
