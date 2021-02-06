from selenium import webdriver

import csv_loader
import urllib2
import lxml.html
import csv
import sys

browser = webdriver.Chrome("c:\\workspace\\python\\chromedriver.exe")


# Download a webpage and return the inner html as a string
def download_webpage(url):
    global browser
    # browser = webdriver.Chrome()
    browser.get(url)
    return browser.execute_script("return document.body.innerHTML")


# Take the inner html as a string and convert it into an array of cards
def parse_webpage(inner_html):
    ret = []

    html = lxml.html.fromstring(inner_html)
    search_result_html = html.get_element_by_id("search-results-table")

    result_list = search_result_html.xpath('//table/tbody/tr')
    result_list.pop(0)

    for result in result_list:
        obj = {}

        card_name = result.xpath("./td/strong/a/text()")[0]
        card_name = card_name.replace("\n", "")
        card_name = card_name.strip()
        obj["name"] = card_name

        set_name = result.xpath("./td[2]/div[1]/text()")[0]
        set_name = set_name.replace("\n", "")
        set_name = set_name.strip()

        splited_set_name = set_name.split("  ")
        set_name = splited_set_name[0]
        obj["set"] = set_name

        if len(splited_set_name) > 1:
            obj["foil"] = True
        else:
            obj["foil"] = False

        price = result.xpath("./td[3]/div[2]/strong/text()")[0]
        price = price.replace("\n", "")
        price = price.strip()
        price = price.split(" ")[0]
        obj["tix"] = price

        ret.append(obj)

    return ret


# Build a search urls for cardhoarder.com
def build_cardhoarder_url(set_name_id, card_name, foil):
    encoded_name = urllib2.quote(card_name)

    if foil:
        foil_filter = "1"
    else:
        foil_filter = "0"

    url = "https://www.cardhoarder.com/cards/index/sort:relevance/viewtype:detailed?data%5Bsearch%5D=" + encoded_name + "&data%5Bsets%5D%5B0%5D=" + set_name_id + "&data%5Bis_foil%5D=" + foil_filter
    return url


# Search for a given card in an array of card
def get_card(cards_array, card_name, set_name, foil):
    card = None
    for result in cards_array:
        if result["name"].lower() == card_name.lower() and result["set"].lower() == set_name.lower() and result["foil"] is foil:
            card = result
            break

    return card


# Search for a card and return its description
def get_card_description(card_name, set_name_id, set_name, foil):
    url = build_cardhoarder_url(set_name_id, card_name, foil)
    inner_html = download_webpage(url)
    results_list = parse_webpage(inner_html)
    return get_card(results_list, card_name, set_name, foil)


# Return the price for a card
def get_price_tix(card_name, set_name_id, set_name, foil):
    card = get_card_description(card_name, set_name_id, set_name, foil)
    return card["tix"]


def add_price_to_csv(csv_filename, cards):
    f = open(csv_filename)
    data = [item for item in csv.reader(f)]
    f.close()

    for row in data:

        name = row[1]
        if name is None or name == "":
            continue

        filter_row = row[4]
        if filter_row is None or filter_row == "" or filter_row == "0":
            [item for item in cards if item.get('name') == name]
            if item is None or len(item) == 0:
                continue

            row.append(item["tix"])

    f = open(csv_filename, 'w')
    csv.writer(f).writerows(data)
    f.close()


argCount = len(sys.argv)
if argCount != 4:
    print "Wrong number of arguments"
    exit(1)

# SET_NAME_ID = "M19"
# SET_NAME = "Core Set 2019"
# CSV_FILENAME = "c:\\card\\csv\M19_Wanted.csv"

SET_NAME_ID = sys.argv[1]  # XLN, M19, etc
SET_NAME = sys.argv[2]  # Ixalan, Core Set 19
CSV_FILENAME = sys.argv[3]  # "c:\\card\\csv\M19_Wanted.csv"

card_name_array = csv_loader.load_csv(CSV_FILENAME)

all_cards = []
# add_price_to_csv(CSV_FILENAME, all_cards)
for card in card_name_array:

    card_description = get_card_description(card.strip(), SET_NAME_ID, SET_NAME, False)
    if card_description is None:
        print "ERROR : can't find card %s" % card.strip()
    else:
        all_cards.append(card_description)

browser.close()

sorted_cards = sorted(all_cards, key=lambda k: float(k["tix"]))

price_sum = 0
for card in sorted_cards:
    print "%s : %s tix" % (card["name"], card["tix"])
    price_sum += float(card["tix"])

print "total " + str(price_sum) + " tix"

# add_price_to_csv(CSV_FILENAME, all_cards)
