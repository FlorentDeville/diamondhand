from selenium import webdriver

import csv_loader
import urllib2
import lxml.html


# Download a webpage and return the inner html as a string
def download_webpage(url):
    global browser
    # browser = webdriver.Chrome()
    browser.get(url)
    return browser.execute_script("return document.body.innerHTML")


# Take the inner html as a string and return the price of the card
def get_price_from_webpage(inner_html):
    html = lxml.html.fromstring(inner_html)

    result = html.xpath("//span[contains(@class, 'price')]")

    price = result[0].text
    # splitted_price = price.split(' ')
    clean_price = price.replace('$', '')
    return clean_price


# Build a search urls for cardhoarder.com
def build_mtgo_url(set_name_id, card_name):
    clean_card_name = card_name.replace(' ', '_')
    clean_card_name = clean_card_name.replace('\'', '')
    clean_card_name = clean_card_name.replace(',', '')

    url = "https://www.mtgotraders.com/store/" + set_name_id + "_" + clean_card_name + ".html"
    return url


browser = webdriver.Chrome("c:\\workspace\\python\\chromedriver.exe")

SET_NAME_ID = "M19"
SET_NAME = "Core Set 2019"

card_name_array = csv_loader.load_csv("c:\\card\\csv\M19_Wanted.csv")
# card_name_array = ["Stitcher's Supplier"]

all_cards = []
for card in card_name_array:
    url = build_mtgo_url(SET_NAME_ID, card)
    html = download_webpage(url)
    price = get_price_from_webpage(html)

    card_description = {}
    card_description['name'] = card
    card_description['price'] = float(price)

    all_cards.append(card_description)

sorted_cards = sorted(all_cards, key=lambda k: k["price"])

price_sum = 0
for card in sorted_cards:
    print "%s : %s $" % (card["name"], card["price"])
    price_sum += float(card["price"])

print "total " + str(price_sum) + " $"


browser.close()
