from selenium import webdriver

import csv_loader
import json
import pprint
import time
import urllib2
import lxml.html

MODE_SAVE_SELLER_DB = 0
MODE_USE_SELLER_DB = 1
MODE_USE_ONLINE_SELLER_DB = 2
#####################################################
#                  CONFIG                           #
#csv_filename = "C:\\card\\csv\\FULL.csv"
csv_filename = "C:\\card\\csv\\KAMIGAWA.csv"
json_filename = csv_filename + ".json"
onlyNearMint = True
onlyTcgPlayerDirect = False
masterSet = "chk"
#masterSet = None
seller_db_mode = MODE_USE_SELLER_DB
#seller_db_mode = MODE_SAVE_SELLER_DB

#####################################################

enableNearMint = False
enableTcgPlayerDirect = False


# Download a webpage and return the inner html as a string
def download_webpage(url):
    global browser
    global onlyNearMint
    global onlyTcgPlayerDirect
    global enableNearMint
    global enableTcgPlayerDirect

    browser.get(url)

    # check the near mint check box
    if onlyNearMint and not enableNearMint:
        button = browser.find_element_by_xpath("//a[contains(@onclick, 'NearMint')]")
        button.click()
        time.sleep(1)
        enableNearMint = True

    if onlyTcgPlayerDirect and not enableTcgPlayerDirect:
        button = browser.find_element_by_xpath("//a[contains(@onclick, 'WantDirect')]")
        button.click()
        time.sleep(2)
        enableTcgPlayerDirect = True

    return browser.execute_script("return document.body.innerHTML")


# Take the inner html as a string and return the price of the card
def get_sellers_from_webpage(inner_html):
    html = lxml.html.fromstring(inner_html)

    sellers_list = []

    all_names = html.xpath("//div[contains(@class, 'product-listing')]/div[contains(@class, 'product-listing__seller')]/div/a")
    all_prices = html.xpath("//div[contains(@class, 'product-listing')]/div[contains(@class, 'product-listing__pricing')]/span[contains(@class, 'product-listing__price')]")

    if len(all_names) != len(all_prices):
        print "ERROR : mismatch between the number of prices and sellers"
        exit(1)

    for ii in range(len(all_names)):
        seller_info = {}
        seller_info["name"] = all_names[ii].text
        seller_info["price"] = all_prices[ii].text.replace('$', '')
        sellers_list.append(seller_info)

    return sellers_list


def get_tcgplayer_id(set_code):
    has_more = True
    card_list_url = "https://api.scryfall.com/cards/search?order=set&q=e:" + set_code + "&unique=prints"

    card_list = []
    while has_more:
        request = urllib2.Request(card_list_url)
        response = urllib2.urlopen(request)
        raw_result = response.read()
        result = json.loads(raw_result)
        card_list = card_list + result["data"]
        has_more = result["has_more"]
        if has_more:
            card_list_url = result["next_page"]

    return card_list


def search_card_in_full_set(full_set, col_number):
    for item in full_set:
        if item["collector_number"] == col_number:
            return item

    return None


# Sort the cards per seller and sort by the seller selling the most cards
def analyze_find_best_single_seller(seller_db, full_cards):

    # count the number of available cards per sellers
    print "Count cards per sellers..."
    seller_count = {}
    for tcgid in seller_db:
        for seller in seller_db[tcgid]:

            # don't add cards above 5$
            price = float(seller["price"])
            name = seller["name"]

            if price >= 5:
                continue

            if name not in seller_count:
                seller_count[name] = []

            info = {}
            info["tcg_id"] = tcgid
            info["price"] = price
            seller_count[name].append(info)

    print "Compute total prices..."
    seller_total_price = {}
    for seller_name in seller_count:
        seller_total_price[seller_name] = 0
        for card_info in seller_count[seller_name]:
            price = card_info["price"]
            seller_total_price[seller_name] += float(price)

    print "Filter out sellers below $5..."
    #PRICE_THRESHOLD = 5
    #filtered_seller = {}
    #for seller_name in seller_count:
    #    if seller_total_price[seller_name] >= PRICE_THRESHOLD:
    #        filtered_seller[seller_name] = seller_count[seller_name]
    filtered_seller = seller_count

    if masterSet is not None:
        # sort seller by number of cards in the master set
        print "Sorting by master set " + masterSet + "..."

        # count number of cards from the master set
        masterSetCardCount = {}
        for seller_name in filtered_seller:
            masterSetCount = 0
            for cardInfo in filtered_seller[seller_name]:
                tcgplayerid = int(cardInfo["tcg_id"])
                set_name = full_cards[tcgplayerid]["set"]
                if set_name == masterSet:
                    masterSetCount += 1

            masterSetCardCount[seller_name] = masterSetCount

        # sort by master set card count
        sortedMasterSetCardCount = sorted(masterSetCardCount.items(), key=lambda key: key[1], reverse=True)

        sorted_sellers = []
        for seller in sortedMasterSetCardCount:
            sellerName = seller[0]
            item = []
            item.append(sellerName)
            item.append(filtered_seller[sellerName])
            sorted_sellers.append(item)
    else:
        # sort by the number of cards per sellers
        print "Sort sellers by card quantity..."
        sorted_sellers = sorted(filtered_seller.items(), key=lambda key: len(key[1]), reverse=True)

    # print results
    print "---RESULT---"
    for seller in sorted_sellers:
        price_sum = 0
        print seller[0]
        for card_info in seller[1]:
            tcgplayerid = int(card_info["tcg_id"])
            price = card_info["price"]

            name = full_cards[tcgplayerid]["name"]
            col_number = full_cards[tcgplayerid]["collector_number"]
            set_name = full_cards[tcgplayerid]["set"]
            # print "    " + str(col_number) + " " + set_name + " " + name + " " + str(price)
            print('{:<3} {:<3} {:<45} {:>6}'.format(col_number, set_name, name, price))
            price_sum = price_sum + float(price)

        print "    TOTAL=" + str(price_sum)


# Keep the cheapest cards
def analyze_tcgplayer_direct(seller_db, full_cards):
    # sort by the cheapest cards first
    print "---RESULT---"
    price_sum = 0
    for tcgplayerid in seller_db:
        first_seller = seller_db[tcgplayerid][0]

        price_sum = price_sum + float(first_seller["price"])

        card = full_cards[tcgplayerid]

        price = first_seller["price"]

        name = full_cards[tcgplayerid]["name"]
        col_number = full_cards[tcgplayerid]["collector_number"]
        set_name = full_cards[tcgplayerid]["set"]
        # print "    " + str(col_number) + " " + set_name + " " + name + " " + str(price)
        print('{:<3} {:<3} {:<20} {:>6}'.format(col_number, set_name, name, price))

        # print card["set"] + " " + card["name"] + " " + first_seller["name"] + " " + first_seller["price"]

    print "TOTAL=" + str(price_sum)


# Find card_needed in full_set_cards
def find_needed_cards_full_description(full_set_cards, card_needed):
    set_code = card_needed["code"]
    col_number = card_needed["col_number"]

    print "    " + set_code + "|" + str(col_number) + "..."

    card = search_card_in_full_set(full_set_cards[set_code], col_number)
    if card is None:
        print "ERROR : Can't find " + set_code + " " + str(col_number) + " in full set"
        exit(1)

    return card


def find_sellers(full_set_cards, cards_needed_array, out_full_cards_needed, out_sellers_db):
    print "Load sellers:"
    for card_needed in cards_needed_array:
        card = find_needed_cards_full_description(full_set_cards, card_needed)
        print "        " + card["name"] + "..."

        if "tcgplayer_id" not in card:
            print "        No tcgplayer id"
            continue

        tcgplayerid = card["tcgplayer_id"]
        out_full_cards_needed[tcgplayerid] = card

        tcgplayer_url = "https://shop.tcgplayer.com/product/productsearch?id=" + str(tcgplayerid)
        html = download_webpage(tcgplayer_url)
        sellers = get_sellers_from_webpage(html)

        print "        " + str(len(sellers)) + " sellers found."

        if len(sellers) == 0:
            continue

        out_sellers_db[tcgplayerid] = sellers


print "---SETUP---"
print "   only near mint=" + str(onlyNearMint)
print "   only tcg player direct mint=" + str(onlyTcgPlayerDirect)
print "   master set=" + str(masterSet)
print "   seller db mode=" + str(seller_db_mode)
print "-----------"
# load the cards I need
# {
#   code
#   col_number
# }
print "Load csv..."
cards_needed_array = csv_loader.load_list_csv(csv_filename)

print "Setup webdriver..."
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--start-maximized")
browser = webdriver.Chrome(executable_path="c:\\workspace\\python\\chromedriver.exe", chrome_options=chromeOptions)

# load the full set from scryfall
print "Load full set..."
full_set_cards = {}  # full_set_cards[set_code]
for card in cards_needed_array:
    set_code = card["code"]
    if set_code not in full_set_cards:
        print "    Load " + set_code + "..."
        full_set_cards[set_code] = get_tcgplayer_id(set_code)

seller_db = {}
full_cards_needed = {}
if seller_db_mode == MODE_SAVE_SELLER_DB:
    find_sellers(full_set_cards, cards_needed_array, full_cards_needed, seller_db)
    with open(json_filename, "w") as out_file:
        json.dump(seller_db, out_file, indent=4)

    browser.close()
    exit(0)
elif seller_db_mode == MODE_USE_SELLER_DB:
    with open(json_filename) as read_file:
        seller_db = json.load(read_file)

    for card_needed in cards_needed_array:
        card = find_needed_cards_full_description(full_set_cards, card_needed)
        print "        " + card["name"] + "..."

        if "tcgplayer_id" not in card:
            print "        No tcgplayer id"
            continue

        tcgplayerid = card["tcgplayer_id"]
        full_cards_needed[tcgplayerid] = card

elif seller_db_mode == MODE_USE_ONLINE_SELLER_DB:
    find_sellers(full_set_cards, cards_needed_array, full_cards_needed, seller_db)

if onlyTcgPlayerDirect:
    analyze_tcgplayer_direct(seller_db, full_cards_needed)
else:
    analyze_find_best_single_seller(seller_db, full_cards_needed)

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(sorted_sellers)

browser.close()
