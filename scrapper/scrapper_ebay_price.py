import csv
import os
from datetime import datetime

import lxml.html
from selenium import webdriver


class ScrapperEbayPrice:
    m_browser = None

    def __init__(self, browser):
        self.m_browser = browser

    def get_sold_prices(self, url, start_date=None):
        self.m_browser.get(url)
        inner_html = self.m_browser.execute_script("return document.body.innerHTML")
        html = lxml.html.fromstring(inner_html)

        xpath_sold_item = "//ul[contains(@class, 'srp-results')]/li"
        sold_items_element = html.xpath(xpath_sold_item)

        ret = []
        for sold_item in sold_items_element:
            xpath_date = ".//div/div[2]/div[2]/div/span/span"
            date_element = sold_item.xpath(xpath_date)
            raw_date_text = date_element[0].text
            date_text = raw_date_text[6:]

            #/html/body/div[4]/div[4]/div[2]/div[1]/div[2]/ul/li[15]/div/div[2]/div[5]/span/span
            xpath_time = ".//div/div[2]/div[contains(@class, 's-item__details')]/span/span"
            time_element = sold_item.xpath(xpath_time)
            raw_time_text = time_element[0].text
            time_text = raw_time_text.split(' ')[1]

            date = datetime.strptime(date_text + " " + time_text, '%b %d, %Y %H:%M')

            if start_date is not None and date <= start_date:
                continue

            xpath_price = ".//div/div[2]/div[contains(@class, 's-item__details')]/div[1]/span/span"
            price_element = sold_item.xpath(xpath_price)
            raw_price = price_element[0].text
            price = float(raw_price[1:])

            xpath_shipping = ".//div/div[2]/div[contains(@class, 's-item__details')]/div[contains(@class, 's-item__detail')]/span[contains(@class, 's-item__shipping')]"
            shipping_element = sold_item.xpath(xpath_shipping)
            raw_shipping = shipping_element[0].text
            raw_shipping_price = "+$0.00"
            if raw_shipping != "Free shipping":
                size = len(raw_shipping)
                bad_text = " shipping"
                bad_text_size = len(bad_text)
                raw_shipping_price = raw_shipping[0:size-bad_text_size]

            shipping_price = float(raw_shipping_price[2:])

            total_price = price + shipping_price

            newPrice = {}
            newPrice["date"] = date
            newPrice["price"] = total_price
            ret.append(newPrice)

        return ret


if __name__ == "__main__":
    print "Setup webdriver..."
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--start-maximized")
    browser = webdriver.Chrome(executable_path="C:/workspace/python/chromedriver.exe", chrome_options=chromeOptions)

    csvFilename = "C:\\workspace\\python\\data\kaldheim_draft_booster_box.csv"

    entries = []

    lastDate = None
    if os.path.exists(csvFilename):
        with open(csvFilename) as csvFile:
            lines = csv.reader(csvFile, delimiter=';', quotechar='"')
            for line in lines:
                date = datetime.strptime(line[0], '%Y-%m-%d %H:%M:%S')
                newEntry = {}
                newEntry["date"] = date
                newEntry["price"] = line[1]
                entries.append(newEntry)

        lastDate = entries[len(entries)-1]["date"]

    scrapper = ScrapperEbayPrice(browser)

    url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=kaldheim+booster+box+-set+-collector+-bundle+-theme+-repack+-error+-code+-repacked+-promo+-case+-collectors+-%22ice+age%22+-prerelease&_sacat=0&LH_TitleDesc=0&LH_PrefLoc=1&LH_Complete=1&rt=nc&LH_Sold=1&_ipg=200"
    res = scrapper.get_sold_prices(url, lastDate)

    with open(csvFilename, "a") as f:
        for price in reversed(res):
            new_line = "\"{}\";{}\n"
            new_line = new_line.format(price["date"], price["price"])

            f.write(new_line)

    print "Over"
    browser.close()
