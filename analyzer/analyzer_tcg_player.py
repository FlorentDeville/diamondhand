import sys
sys.path.append('C:/workspace/python')
from selenium import webdriver

from db.db_buylist import load_buylist
from db.db_fftcg import DbFFTcg
from scrapper.scrapper_tcg_price import ScrapperTcgPrice


# Sort the cards per seller and sort by the seller selling the most cards
def analyze_find_best_single_seller(all_prices, cards_needed):

    seller_shipping_info = {}

    # count the number of available cards per sellers
    print "Count cards per sellers..."
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

            if price >= 5:
                continue

            if name not in seller_count:
                seller_count[name] = []

            info = {}
            info["card_id"] = card_id
            info["price"] = price
            seller_count[name].append(info)

    print "Compute total prices..."
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

    print "Sort sellers by card quantity..."
    sorted_sellers = sorted(filtered_seller.items(), key=lambda key: len(key[1]), reverse=True)

    # print results
    print "---RESULT---"
    for seller in sorted_sellers:
        price_sum = 0
        diff_sum = 0
        seller_name = seller[0]
        print seller_name

        #sort cards per number
        sorted_cards = sorted(seller[1], key=lambda entry: entry["card_id"])
        card_count = len(sorted_cards)
        for card_info in sorted_cards:
            id = card_info["card_id"]
            price = card_info["price"]

            card = cards_needed[id]
            name = card.name
            col_number = card.number
            set_name = card.set_name
            diff = price - all_prices[id][0].m_price
            print('{:<3} {:<3} {:<45} {:>6} {:+.2f}'.format(col_number, set_name, name, price, diff))
            price_sum = price_sum + float(price)
            diff_sum = diff_sum + diff

        percent = diff_sum / price_sum * 100

        if seller_shipping_info[seller_name]["shipping_free_over_5"] and price_sum >= 5:
            print "Shipping: Free over $5"
        elif seller_shipping_info[seller_name]["shipping_free_over_35"] and price_sum >= 35:
            print "Shipping: Free over $35"
        else:
            shipping = seller_shipping_info[seller_name]["shipping"]
            print "Shipping: " + str(shipping)
            price_sum = price_sum + shipping

        print str(card_count) + " TOTAL=" + str(price_sum) + " (" + "{:+.2f}".format(diff_sum) + " " + "{:+.2f}%".format(percent) + ")"


# Keep the cheapest cards
def analyze_tcgplayer_direct(seller_db, full_cards):
    # sort by the cheapest cards first
    print "---RESULT---"
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
        print('{:<3} {:<3} {:<20} {:>6}'.format(col_number, set_name, name, price))

    print "TOTAL=" + str(price_sum)


def print_help():
    print "analyzer:"
    print "Mandatory argument:"
    print "    -buylist-id <id> : id of the buylist to use"
    print "Optional argument:"
    print "    -direct : only use tcgplayer direct sellers"
    print "    -help : print this help text"


if __name__ == "__main__":

    tcgDirect = False
    buylist_ids = []
    argc = len(sys.argv)
    index = 0
    #for arg in sys.argv:
    #for index in range(argc):
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
        elif arg == "-help":
            print_help()
            exit(0)

        index = index + 1

    if len(buylist_ids) == 0:
        print_help()
        exit(0)

    print "Setup webdriver..."
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

    print "Scrap prices..."
    nearMint = True
    scrapper = ScrapperTcgPrice(browser, nearMint, tcgDirect)

    all_prices = {}
    for card_id in cards_needed:
        card = cards_needed[card_id]
        print "    Scrap " + card.name + "..."
        prices = scrapper.get_prices(card)
        all_prices[card.id] = prices

    if tcgDirect:
        analyze_tcgplayer_direct(all_prices, cards_needed)
    else:
        analyze_find_best_single_seller(all_prices, cards_needed)

    browser.close()
    browser.quit()
    print "Over"
