import time
import lxml.html

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
        url = dbEntry.tcg_url
        html = self.__download_webpage(url)
        sellers = self.__get_sellers_from_webpage(html)

        prices = []
        for seller in sellers:
            newPrice = Price()
            newPrice.m_id = dbEntry.id
            newPrice.m_price = float(seller["price"])
            newPrice.m_sellerName = seller["name"]
            prices.append(newPrice)

        return prices

    # Download a webpage and return the inner html as a string
    def __download_webpage(self, url):
        self.m_browser.get(url)

        # check the near mint check box
        if self.m_onlyNearMint and not self.m_enableNearMint:
            button = browser.find_element_by_xpath("//a[contains(@onclick, 'NearMint')]")
            button.click()
            time.sleep(1)
            self.m_enableNearMint = True

        if self.m_onlyTcgPlayerDirect and not self.m_enableTcgPlayerDirect:
            button = browser.find_element_by_xpath("//a[contains(@onclick, 'WantDirect')]")
            button.click()
            time.sleep(2)
            self.m_enableTcgPlayerDirect = True

        return browser.execute_script("return document.body.innerHTML")

    # Take the inner html as a string and return the list of prices
    def __get_sellers_from_webpage(self, inner_html):
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


if __name__ == "__main__":
    print "Setup webdriver..."
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--start-maximized")
    browser = webdriver.Chrome(executable_path="C:/workspace/python/chromedriver.exe", chrome_options=chromeOptions)

    print "Load csv..."
    ffdb = DbFFTcg(browser, "C:\\workspace\\python\\fftcg\\db.csv")
    entries = ffdb.load()

    print "Scrap prices..."
    nearMint = True
    tcgDirect = False
    scrapper = ScrapperTcgPrice(browser, nearMint, tcgDirect)

    for ii in range(0, 10):
        singleEntry = entries[ii]
        print "scrap " + singleEntry.name + "..."

        prices = scrapper.get_prices(singleEntry)
        for price in prices:
            print "   " + str(price.m_price) + " " + price.m_sellerName

    print "Over"
    browser.close()
