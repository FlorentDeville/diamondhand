import json
import time
import urllib2

EXTENSION_M19 = "m19"
CARDS_M19 = [3, 9, 23, 27, 33, 34, 65, 67, 68, 69, 76, 77, 79, 88, 90, 91, 92, 99, 102, 104, 106, 114, 121, 128, 129, 130, 134, 135, 136, 144, 145, 149, 152, 154, 155, 179, 185, 186, 196, 200, 201, 203, 207, 208, 212, 214, 215, 218, 219, 220, 222, 223, 225, 229, 230, 232, 235, 249]
# CARDS_M19 = [3]


EXTENSION_KLD = "kld"
CARDS_KLD = [4, 67, 96, 110, 112, 163, 184, 186]


def download_cards(extension_code, card_number_array):
    results = []
    for card_number in card_number_array:
        url = "https://api.scryfall.com/cards/" + extension_code + "/" + str(card_number)
        print "Querying " + extension_code + " " + str(card_number) + "..."
        json_string = urllib2.urlopen(url).read()
        obj = json.loads(json_string)
        results.append(obj)
        time.sleep(0.1)

    return results


def report_tix(extension_code, card_number_array):
    raw_cards = download_cards(extension_code, card_number_array)

    total_price = compute_price_tix(raw_cards)
    print "%s missing card costs : %f tix" % (extension_code, total_price)

    print_cheapest_card(raw_cards)


def compute_price_tix(cards):
    price_sum = 0
    for card in cards:
        price = card["tix"]
        price_sum += float(price)

    return price_sum


def get_price_tix(card):
    return float(card["tix"])


def print_cheapest_card(cards):
    sorted_cards = sorted(cards, key=get_price_tix)
    for card in sorted_cards:
        print "    %s : %s tix" % (card["name"], card["tix"])


def m19():
    report_tix(EXTENSION_M19, CARDS_M19)


def kld():
    kld_cards = download_cards(EXTENSION_KLD, CARDS_KLD)
    price_sum = 0
    for card in kld_cards:
        price = card["usd"]
        price_sum += float(price)

        print "    %s : %s usd" % (card["name"], price)

    print "kld missing card costs : %f usd" % price_sum


m19()
# kld()
