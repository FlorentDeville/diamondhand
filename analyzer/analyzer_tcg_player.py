import json
import logging
import sys
sys.path.append('C:/workspace/python')
from selenium import webdriver

from db.db_buylist import load_buylist
from scrapper.scrapper_tcg_price import ScrapperTcgPrice


# Sort the cards per seller and sort by the seller selling the most cards
def analyze_find_best_single_seller(all_prices, cards_needed):

    seller_shipping_info = {}

    # count the number of available cards per sellers
    logging.debug("Count cards per sellers...")
    seller_count = {}
    for card_id in all_prices:
        card_sellers = all_prices[card_id]
        for seller in card_sellers:

            # don't add cards above 5$
            price = float(seller.m_price)
            name = seller.m_sellerName

            if name not in seller_shipping_info:
                seller_shipping_info[name] = {}
                seller_shipping_info[name]["shipping"] = seller.m_shipping
                seller_shipping_info[name]["shipping_free_over_5"] = seller.m_free_shipping_over_5
                seller_shipping_info[name]["shipping_free_over_35"] = seller.m_free_shipping_over_35

            if name not in seller_count:
                seller_count[name] = []

            info = {}
            info["card_id"] = card_id
            info["price"] = price
            seller_count[name].append(info)

    logging.debug("Compute total prices...")
    seller_total_price = {}
    for seller_name in seller_count:
        seller_total_price[seller_name] = 0
        for card_info in seller_count[seller_name]:
            price = card_info["price"]
            seller_total_price[seller_name] += float(price)

    #print "Filter out sellers below $5..."
    #PRICE_THRESHOLD = 5
    #filtered_seller = {}
    #for seller_name in seller_count:
    #    if seller_total_price[seller_name] >= PRICE_THRESHOLD:
    #        filtered_seller[seller_name] = seller_count[seller_name]
    filtered_seller = seller_count

    logging.debug("Sort sellers by card quantity...")
    sorted_sellers = sorted(filtered_seller.items(), key=lambda key: len(key[1]), reverse=True)

    # print results
    output = []
    for seller in sorted_sellers:
        price_sum = 0
        diff_sum = 0
        seller_name = seller[0]

        output_seller = {}
        output_seller["seller_name"] = seller[0]
        output_seller["cards"] = []

        #sort cards per number
        sorted_cards = sorted(seller[1], key=lambda entry: entry["card_id"])
        for card_info in sorted_cards:
            id = card_info["card_id"]
            price = card_info["price"]

            card = cards_needed[id]
            name = card.name
            col_number = card.number
            set_name = card.set_name
            diff = price - all_prices[id][0].m_price
            price_sum = price_sum + float(price)
            diff_sum = diff_sum + diff

            output_card = {}
            output_card["name"] = name
            output_card["set_name"] = set_name
            output_card["col_number"] = col_number
            output_card["price"] = price
            output_card["price_dt"] = diff
            output_seller["cards"].append(output_card)

        percent = diff_sum / price_sum * 100

        if seller_shipping_info[seller_name]["shipping_free_over_5"] and price_sum >= 5:
            output_seller["shipping_cost"] = 0
            output_seller["shipping_reason"] = "Free over $5"
        elif seller_shipping_info[seller_name]["shipping_free_over_35"] and price_sum >= 35:
            output_seller["shipping_cost"] = 0
            output_seller["shipping_reason"] = "Free over $35"
        else:
            shipping = seller_shipping_info[seller_name]["shipping"]
            price_sum = price_sum + shipping
            output_seller["shipping_cost"] = shipping
            output_seller["shipping_reason"] = ""

        output_seller["total"] = price_sum
        output_seller["total_dt"] = diff_sum
        output_seller["total_dt_percent"] = percent

        output.append(output_seller)

    return output


# Keep the cheapest cards
def analyze_tcgplayer_direct(seller_db, full_cards):
    # sort by the cheapest cards first
    output = []

    output_seller = {}
    output_seller["seller_name"] = "Direct"
    output_seller["cards"] = []
    output_seller["shipping_cost"] = 0
    output_seller["shipping_reason"] = "Free over $35"

    price_sum = 0
    for card_id in seller_db:
        list_seller = seller_db[card_id]
        if len(list_seller) == 0:
            continue

        first_seller = seller_db[card_id][0]

        price = first_seller.m_price
        price_sum = price_sum + float(price)

        name = full_cards[card_id].name
        col_number = full_cards[card_id].number
        set_name = full_cards[card_id].set_name
        #print('{:<3} {:<3} {:<20} {:>6}'.format(col_number, set_name, name, price))

        output_card = {}
        output_card["name"] = name
        output_card["set_name"] = set_name
        output_card["col_number"] = col_number
        output_card["price"] = price
        output_card["price_dt"] = 0
        output_seller["cards"].append(output_card)

    output_seller["total"] = price_sum
    output_seller["total_dt"] = 0
    output_seller["total_dt_percent"] = 0
    output.append(output_seller)
    return output


# Print the result as a json string
def print_output_json(result):
    json_output = json.dumps(result)
    logging.info(json_output)


# Pretty print the result
def print_output_pretty(result):
    print "---RESULT---"
    for seller in result:
        print (seller["seller_name"].encode("utf-8"))

        for card_info in seller["cards"]:
            col_number = card_info["col_number"]
            set_name = card_info["set_name"]
            name = card_info["name"]
            price = card_info["price"]
            diff = card_info["price_dt"]
            print('{:<3} {:<3} {:<45} {:>6} {:+.2f}'.format(col_number, set_name, name, price, diff))

        if seller["shipping_cost"] == 0:
            print "Shipping: " + seller["shipping_reason"]
        else:
            print "Shipping: " + str(seller["shipping_cost"])

        card_count = len(seller["cards"])
        price_sum = seller["total"]
        diff_sum = seller["total_dt"]
        percent = seller["total_dt_percent"]
        print str(card_count) + " TOTAL=" + str(price_sum) + " (" + "{:+.2f}".format(diff_sum) + " " + "{:+.2f}%".format(percent) + ")"


def print_help():
    print "analyzer:"
    print "Mandatory argument:"
    print "    -buylist-id <id> : id of the buylist to use"
    print "Optional argument:"
    print "    -direct : only use tcgplayer direct sellers"
    print "    -output-format <json|pretty> : the output format, json or pretty print. Default format is pretty."
    print "    -log-level <DEBUG> : change the level of logs to print"
    print "    -help : print this help text"


if __name__ == "__main__":

    logging.basicConfig(level=logging.CRITICAL)

    tcgDirect = False
    buylist_ids = []
    argc = len(sys.argv)
    index = 0
    OUTPUT_FORMAT_JSON = 0
    OUTPUT_FORMAT_PRETTY = 1
    output_format = OUTPUT_FORMAT_PRETTY

    while index < argc:
        arg = sys.argv[index]
        if arg == "-buylist-id":
            index = index + 1
            if index >= argc:
                print "Missing value for argument -buylist-id"
                exit(1)
            else:
                buylist_ids.append(sys.argv[index])
        elif arg == "-direct":
            tcgDirect = True
        elif arg == "-output-format":
            index = index + 1
            if index >= argc:
                print "Missing value for argument -output-mode"
                exit(1)
            else:
                mode = sys.argv[index]
                if mode == "json":
                    output_format = OUTPUT_FORMAT_JSON
                elif mode == "pretty":
                    output_format = OUTPUT_FORMAT_PRETTY
                else:
                    print "Unknow output mode " + mode
                    print_help()
                    exit(1)
        elif arg == "-help":
            print_help()
            exit(0)
        elif arg == "-log-level":
            index = index + 1
            if index >= argc:
                print "Missing value for argument -log-level"
                exit(1)
            else:
                log_level = sys.argv[index]
                if log_level == "DEBUG":
                    logging.basicConfig(level=logging.DEBUG)

        index = index + 1

    if len(buylist_ids) == 0:
        print_help()
        exit(0)

    logging.debug("Setup webdriver...")
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--start-maximized")
    chromeOptions.add_argument("--log-level=0")
    browser = webdriver.Chrome(executable_path="C:/workspace/python/chromedriver.exe", chrome_options=chromeOptions)

    entries = []
    for id in buylist_ids:
        buylist_entries = load_buylist(id)
        entries = entries + buylist_entries

    cards_needed = {}
    for single_card in entries:
        if single_card.own is True:
            continue
        cards_needed[single_card.id] = single_card

    logging.debug("Scrap prices...")
    nearMint = True
    scrapper = ScrapperTcgPrice(browser, nearMint, tcgDirect)

    all_prices = {}
    for card_id in cards_needed:
        card = cards_needed[card_id]
        logging.debug("    Scrap " + card.name + "...")
        prices = scrapper.get_prices(card.id, card.tcg_url)
        all_prices[card.id] = prices

    result = None
    if tcgDirect:
        result = analyze_tcgplayer_direct(all_prices, cards_needed)
    else:
        result = analyze_find_best_single_seller(all_prices, cards_needed)

    if result is not None:
        if output_format == OUTPUT_FORMAT_JSON:
            print_output_json(result)
        elif output_format == OUTPUT_FORMAT_PRETTY:
            print_output_pretty(result)

    browser.close()
    browser.quit()
    print "Over"
