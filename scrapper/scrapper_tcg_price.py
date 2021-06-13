import argparse
import json
import mysql.connector
import time
import lxml.html
import re

from scrapper.price import Price
from selenium import webdriver


class ScrapperTcgPrice:
    m_onlyNearMint = True
    m_onlyTcgPlayerDirect = False

    m_enableNearMint = False
    m_enableTcgPlayerDirect = False
    m_browser = None

    def __init__(self, browser, onlyNearMint, onlyTcgPlayerDirect):
        self.m_onlyNearMint = onlyNearMint
        self.m_onlyTcgPlayerDirect = onlyTcgPlayerDirect
        self.m_browser = browser

    def get_prices(self, card_id, card_tcg_url):
        prices = []
        url = card_tcg_url
        if url is None or url == "":
            print "        No Url."
            return prices

        html = self.__download_webpage(url)
        sellers = self.__get_sellers_from_webpage(html)

        for seller in sellers:
            newPrice = Price()
            newPrice.m_id = card_id
            newPrice.m_price = float(seller["price"].replace(',', ''))
            newPrice.m_sellerName = seller["name"]
            newPrice.m_shipping = seller["shipping"]
            newPrice.m_free_shipping_over_5 = seller["free_shipping_over_5"]
            newPrice.m_free_shipping_over_35 = seller["free_shipping_over_35"]
            prices.append(newPrice)

        return prices

    def get_normal_market_prices(self, card_tcg_url):
        if card_tcg_url is None or card_tcg_url == "":
            print "        No Url."
            return None

        html = self.__download_webpage(card_tcg_url)
        price = self.__get_normal_market_price_from_webapge(html)
        return price

    def save(self, prices, filename):
        with open(filename, "w") as out_file:
            json.dump(prices, out_file, indent=4)

    # Download a webpage and return the inner html as a string
    def __download_webpage(self, url):
        self.m_browser.get(url)
        time.sleep(2)

        # check the near mint check box
        if self.m_onlyNearMint and not self.m_enableNearMint:
            xpath = "//span[contains(@id, 'NearMint-filter-label')]"
            button = self.m_browser.find_element_by_xpath(xpath)
            button.click()
            time.sleep(1)
            #self.m_enableNearMint = True

        if self.m_onlyTcgPlayerDirect and not self.m_enableTcgPlayerDirect:
            xpath = "//label[contains(@aria-labelledby, 'direct-seller-filter')]"
            button = self.m_browser.find_element_by_xpath(xpath)
            button.click()
            time.sleep(2)
            #self.m_enableTcgPlayerDirect = True

        return self.m_browser.execute_script("return document.body.innerHTML")

    # Take the inner html as a string and return the list of prices
    def __get_sellers_from_webpage(self, inner_html):
        html = lxml.html.fromstring(inner_html)

        sellers_list = []

        xpath_seller_names = "//a[contains(@class, 'seller-info__name')]"
        xpath_prices = "//div[contains(@class, 'listing-item__price')]"

        all_names = html.xpath(xpath_seller_names)
        all_prices = html.xpath(xpath_prices)
        #all_shipping = html.xpath("//div[contains(@class, 'product-listing')]/div[contains(@class, 'product-listing__pricing')]/span[contains(@class, 'product-listing__shipping')]")

        if len(all_names) != len(all_prices):
            print "ERROR : mismatch between the number of prices and sellers"
            exit(1)

        for ii in range(len(all_names)):
            seller_info = {}
            seller_info["name"] = all_names[ii].text
            seller_info["price"] = all_prices[ii].text.replace('$', '')
            seller_info["free_shipping_over_5"] = False
            seller_info["free_shipping_over_35"] = False
            seller_info["shipping"] = 0

            #shippingText = all_shipping[ii].text
            #if "+ Shipping:" in shippingText:
            #    matches = re.search("\+ Shipping: \$(.*)", shippingText)
             #   shippingString = matches.groups()[0]
             #   shipping = float(shippingString)
             #   seller_info["shipping"] = shipping

                #shipping_free = all_shipping[ii].xpath("./span/a")
                #if shipping_free is not None and len(shipping_free) > 0:
                 #   if "Free Shipping on Orders Over $5" in shipping_free[0].text:
                  #      seller_info["free_shipping_over_5"] = True
            #else:
             #   shipping_free = all_shipping[ii].xpath("./a")
              #  if shipping_free is not None and len(shipping_free) > 0:
               #     if "Free Shipping on Orders Over $35" in shipping_free[0].text:
                #        seller_info["free_shipping_over_35"] = True
                 #       seller_info["shipping"] = 1.99
                 #   elif "+ Shipping: Included" in shipping_free[0].text:
                  #      seller_info["shipping"] = 0

            sellers_list.append(seller_info)

        return sellers_list

    # Take the inner html as a string and return the normal market price
    def __get_normal_market_price_from_webapge(self, inner_html):
        html = lxml.html.fromstring(inner_html)
        normal_price = html.xpath("//td[contains(@class, 'price-point__data')]")
        if len(normal_price) == 0:
            print "ERROR: Can't find the normal market price"
            return

        text_price = normal_price[0].text.replace('$', '')
        price = float(text_price)
        return price


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Parse tcgplayer webpage to retrieve price information.")
    parser.add_argument('-c', '--card-id', type=int, dest="card_id", help="Id of the card.")
    parser.add_argument('-sp', '--scrap-seller-prices', dest="scrap_seller_prices", action="store_true", default=False, help="Scrap all the sellers' prices.")
    parser.add_argument('-nmp', '--scrap-normal-market-price', dest="scrap_normal_market_price", action="store_true", default=False, help="Scrap all the sellers' prices.")
    options = parser.parse_args()

    if options.scrap_seller_prices is False and options.scrap_normal_market_price is False:
        parser.print_help()
        exit(1)

    print "Setup webdriver..."
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--start-maximized")
    browser = webdriver.Chrome(executable_path="C:/workspace/python/chromedriver.exe", chrome_options=chromeOptions)

    print "Get information of card " + str(options.card_id) + "..."
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="wallstreet"
    )

    sql = "select card.tcg_url from card where id=" + str(options.card_id)

    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    url = results[0][0]

    nearMint = True
    tcgDirect = False
    scrapper = ScrapperTcgPrice(browser, nearMint, tcgDirect)

    if options.scrap_seller_prices is True:
        print "Scrap prices..."
        prices = scrapper.get_prices(options.card_id, url)
        for price in prices:
            print "      " + str(price.m_price) + " " + price.m_sellerName

    if options.scrap_normal_market_price is True:
        print "Scrap normal market price..."
        market_price = scrapper.get_normal_market_prices(url)
        print" Normal Market Price : $" + str(market_price)

    #print "Saving prices..."
    #pricesDbFilename = "C:\\workspace\\python\\fftcg\\prices.json"
    #scrapper.save(allPrices, pricesDbFilename)

    print "Over"
    browser.close()
    browser.quit()
