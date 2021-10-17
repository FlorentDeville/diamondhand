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
        #"^([a-zA-Z])\d+$"  # H78, H79
    ]

    sub_number = None
    for pattern in patterns_list:
        matches = re.match(pattern, entry.number)
        if matches is None:
            continue

        sub_number = matches.group(1)
        break

    return sub_number


def helper_pokemon_get_sub_set(entry):
    patterns_list = [
        "^([a-zA-Z])\d+$"  # H78, H79
    ]

    sub_set = None
    for pattern in patterns_list:
        matches = re.match(pattern, entry.number)
        if matches is None:
            continue

        sub_set = matches.group(1)
        break

    return sub_set


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


def helper_pokemon_sort_cards(entries):
    card_count = len(entries)

    for ii in range(0, card_count - 1):
        low_card = entries[ii]

        low_card_number = helper_pokemon_get_number(low_card)
        low_card_subnumber = helper_pokemon_get_sub_number(low_card)
        low_card_subset = helper_pokemon_get_sub_set(low_card)

        for jj in range(ii+1, card_count):
            high_card = entries[jj]

            high_card_number = helper_pokemon_get_number(high_card)
            high_card_subnumber = helper_pokemon_get_sub_number(high_card)
            high_card_subset = helper_pokemon_get_sub_set(high_card)

            swap = False

            if low_card_subset is None and high_card_subset is not None:
                pass
            elif low_card_subset is not None and high_card_subset is None:
                swap = True
            elif low_card_subset is not None and high_card_subset is not None:
                if low_card_number > high_card_number:
                    swap = True
            elif low_card_number == high_card_number:
                if low_card_subnumber > high_card_subnumber:
                    swap = True
            elif low_card_number > high_card_number:
                    swap = True

            if swap:
                entries[ii], entries[jj] = entries[jj], entries[ii]
                low_card = entries[ii]
                low_card_number = helper_pokemon_get_number(low_card)
                low_card_subnumber = helper_pokemon_get_sub_number(low_card)
                low_card_subset = helper_pokemon_get_sub_set(low_card)
