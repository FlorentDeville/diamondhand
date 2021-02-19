from selenium import webdriver

from db.db_fftcg import DbFFTcg
from scrapper.scrapper_tcg_price import ScrapperTcgPrice


# Sort the cards per seller and sort by the seller selling the most cards
def analyze_find_best_single_seller(all_prices, cards_needed):

    # count the number of available cards per sellers
    print "Count cards per sellers..."
    seller_count = {}
    for card_id in all_prices:
        card_sellers = all_prices[card_id]
        for seller in card_sellers:

            # don't add cards above 5$
            price = float(seller.m_price)
            name = seller.m_sellerName

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

    print "Filter out sellers below $5..."
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
        print seller[0]
        for card_info in seller[1]:
            id = card_info["card_id"]
            price = card_info["price"]

            card = cards_needed[id]
            name = card.name
            col_number = card.number
            set_name = card.set_name
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


if __name__ == "__main__":
    print "Setup webdriver..."
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--start-maximized")
    browser = webdriver.Chrome(executable_path="C:/workspace/python/chromedriver.exe", chrome_options=chromeOptions)

    print "Load csv..."
    ffdb = DbFFTcg(browser, "C:\\workspace\\python\\fftcg\\db.csv")
    entries = ffdb.load()
    cards_needed = {}
    for ii in range(0, 10):
        cards_needed[entries[ii].id] = entries[ii]

    print "Scrap prices..."
    nearMint = True
    tcgDirect = False
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
    print "Over"
