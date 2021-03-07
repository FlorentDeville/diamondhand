import lxml.html

from db.entry import Entry
from selenium import webdriver


class ScrapperTcgMarketPrice:
    m_browser = None

    def __init__(self, browser):
        self.m_browser = browser

    def get_market_price(self, db_entry):
        self.m_browser.get(db_entry.tcg_url)
        raw_html = self.m_browser.execute_script("return document.body.innerHTML")
        html = lxml.html.fromstring(raw_html)

        market_price_xpath = "/html/body/div[5]/section[2]/div/div[2]/div[1]/table/tbody/tr[1]/td"
        market_price_foil_xpath = "/html/body/div[5]/section[2]/div/div[2]/div[1]/table/tbody/tr[2]/td"

        if db_entry.variation == "foil":
            market_price_element_arr = html.xpath(market_price_foil_xpath)
        else:
            market_price_element_arr = html.xpath(market_price_xpath)

        market_price_raw = market_price_element_arr[0].text
        market_price_cleaned = market_price_raw[1:]
        market_price = float(market_price_cleaned)
        return market_price


if __name__ == "__main__":
    print "Setup webdriver..."
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--start-maximized")
    browser = webdriver.Chrome(executable_path="C:/workspace/python/chromedriver.exe", chrome_options=chromeOptions)

    print "Scrap market prices..."
    nearMint = True
    tcgDirect = False
    scrapper = ScrapperTcgMarketPrice(browser)

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

    price = scrapper.get_market_price(singleEntry)
    print "   " + str(price)

    print "Over"
    browser.close()
    browser.quit()
