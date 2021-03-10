import json
import time
import lxml.html
import re

from db.entry import Entry
from db.db_fftcg import DbFFTcg
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

    def get_prices(self, dbEntry):
        prices = []
        url = dbEntry.tcg_url
        if url is None or url == "":
            print "        No Url."
            return prices

        html = self.__download_webpage(url)
        sellers = self.__get_sellers_from_webpage(html)

        for seller in sellers:
            newPrice = Price()
            newPrice.m_id = dbEntry.id
            newPrice.m_price = float(seller["price"].replace(',', ''))
            newPrice.m_sellerName = seller["name"]
            newPrice.m_shipping = seller["shipping"]
            newPrice.m_free_shipping_over_5 = seller["free_shipping_over_5"]
            newPrice.m_free_shipping_over_35 = seller["free_shipping_over_35"]
            prices.append(newPrice)

        return prices

    def save(self, prices, filename):
        with open(filename, "w") as out_file:
            json.dump(prices, out_file, indent=4)

    # Download a webpage and return the inner html as a string
    def __download_webpage(self, url):
        self.m_browser.get(url)

        # check the near mint check box
        if self.m_onlyNearMint and not self.m_enableNearMint:
            button = self.m_browser.find_element_by_xpath("//a[contains(@onclick, 'NearMint')]")
            button.click()
            time.sleep(1)
            self.m_enableNearMint = True

        if self.m_onlyTcgPlayerDirect and not self.m_enableTcgPlayerDirect:
            button = self.m_browser.find_element_by_xpath("//a[contains(@onclick, 'WantDirect')]")
            button.click()
            time.sleep(2)
            self.m_enableTcgPlayerDirect = True

        return self.m_browser.execute_script("return document.body.innerHTML")

    # Take the inner html as a string and return the list of prices
    def __get_sellers_from_webpage(self, inner_html):
        html = lxml.html.fromstring(inner_html)

        sellers_list = []

        all_names = html.xpath("//div[contains(@class, 'product-listing')]/div[contains(@class, 'product-listing__seller')]/div/a")
        all_prices = html.xpath("//div[contains(@class, 'product-listing')]/div[contains(@class, 'product-listing__pricing')]/span[contains(@class, 'product-listing__price')]")
        all_shipping = html.xpath("//div[contains(@class, 'product-listing')]/div[contains(@class, 'product-listing__pricing')]/span[contains(@class, 'product-listing__shipping')]")

        if len(all_names) != len(all_prices):
            print "ERROR : mismatch between the number of prices and sellers"
            exit(1)

        for ii in range(len(all_names)):
            seller_info = {}
            seller_info["name"] = all_names[ii].text
            seller_info["price"] = all_prices[ii].text.replace('$', '')
            seller_info["free_shipping_over_5"] = False
            seller_info["free_shipping_over_35"] = False

            shippingText = all_shipping[ii].text
            if "+ Shipping:" in shippingText:
                matches = re.search("\+ Shipping: \$(.*)", shippingText)
                shippingString = matches.groups()[0]
                shipping = float(shippingString)
                seller_info["shipping"] = shipping

                shipping_free = all_shipping[ii].xpath("./span/a")
                if shipping_free is not None and len(shipping_free) > 0:
                    if "Free Shipping on Orders Over $5" in shipping_free[0].text:
                        seller_info["free_shipping_over_5"] = True
            else:
                shipping_free = all_shipping[ii].xpath("./a")
                if shipping_free is not None and len(shipping_free) > 0:
                    if "Free Shipping on Orders Over $35" in shipping_free[0].text:
                        seller_info["free_shipping_over_35"] = True
                        seller_info["shipping"] = 1.99
                    elif "+ Shipping: Included" in shipping_free[0].text:
                        seller_info["shipping"] = 0

            sellers_list.append(seller_info)

        return sellers_list


if __name__ == "__main__":
    print "Setup webdriver..."
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--start-maximized")
    browser = webdriver.Chrome(executable_path="C:/workspace/python/chromedriver.exe", chrome_options=chromeOptions)

    print "Load csv..."
    #ffdb = DbFFTcg(browser, "C:\\workspace\\python\\fftcg\\db.csv")
    #entries = ffdb.load()

    print "Scrap prices..."
    nearMint = True
    tcgDirect = False
    scrapper = ScrapperTcgPrice(browser, nearMint, tcgDirect)

    allPrices = []
    #for ii in range(0, 5):
    #singleEntry = entries[ii]
    singleEntry = Entry()
    singleEntry.name = "Blessed Breath"
    singleEntry.number = 1
    singleEntry.rarity = "common"
    singleEntry.id = 1
    singleEntry.set_name = "Champions of Kamigawa"
    singleEntry.tcg_url = "https://shop.tcgplayer.com/magic/champions-of-kamigawa/blessed-breath?id=11948&utm_campaign=affiliate&utm_medium=api&utm_source=scryfall"
    singleEntry.own = False
    singleEntry.set_code = "chk"

    print "   " + singleEntry.name + "..."

    prices = scrapper.get_prices(singleEntry)
    #for price in prices:
    #    print "      " + str(price.m_price) + " " + price.m_sellerName

    #allPrices = allPrices + prices

    #print "Saving prices..."
    #pricesDbFilename = "C:\\workspace\\python\\fftcg\\prices.json"
    #scrapper.save(allPrices, pricesDbFilename)

    print "Over"
    browser.close()
    browser.quit()
