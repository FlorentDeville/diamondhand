import csv
import mysql.connector
import os
import sys
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
            #xpath_date = ".//div/div[2]/div[2]/div/span/span"
            #date_element = sold_item.xpath(xpath_date)
            #raw_date_text = date_element[0].text
            #date_text = raw_date_text[6:]

            #/html/body/div[4]/div[4]/div[2]/div[1]/div[2]/ul/li[15]/div/div[2]/div[5]/span/span
            xpath_time = ".//div/div[2]/div[contains(@class, 's-item__details')]/span/span"
            time_element = sold_item.xpath(xpath_time)
            raw_time_text = time_element[0].text
            #time_text = raw_time_text.split(' ')[1]

            today = datetime.today()
            date = datetime.strptime(raw_time_text + " " + str(today.year), '%b-%d %H:%M %Y')

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


def print_help():
    print "analyzer:"
    print "Mandatory argument:"
    print "    -sealed-product-id <id> : id of the sealed produt to use"
    print "Optional argument:"
    print "    -commit : commit changes to the db"
    print "    -help : print this help text"


if __name__ == "__main__":

    sealed_product_ids = []
    commit = False
    argc = len(sys.argv)
    index = 0
    while index < argc:
        arg = sys.argv[index]
        if arg == "-sealed-product-id":
            index = index + 1
            if index >= argc:
                print "Missing value for argument -sealed-product-id"
                exit(1)
            else:
                sealed_product_ids.append(sys.argv[index])
        elif arg == "-commit":
            commit = True
        elif arg == "-help":
            print_help()
            exit(0)

        index = index + 1

    print "Setup webdriver..."
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--start-maximized")
    browser = webdriver.Chrome(executable_path="C:/workspace/python/chromedriver.exe", chrome_options=chromeOptions)

    db = mysql.connector.connect(host="localhost", user="root", password="", database="wallstreet")

    for sealed_id in sealed_product_ids:
        print "Scrapping " + str(sealed_id) + "..."
        lastDate = None

        #find the last price
        sql = "select s.name, h.date " \
              "from sealed_products as s inner join sealed_products_price_history as h on s.id = h.sealed_product_id " \
              "where s.id=" + str(sealed_id) + " " \
              "order by h.date desc limit 1"

        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) > 0:
            lastDate = datetime.strptime(results[0]["date"], '%Y-%m-%d %H:%M:%S')

        #find the ebay url
        sql = "select ebay_sold_url from sealed_products where id =" + str(sealed_id)
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) <= 0:
            print "ERROR : can't find sealed product with id " + str(sealed_id)
            exit(1)

        url = results[0][0]

        scrapper = ScrapperEbayPrice(browser)
        res = scrapper.get_sold_prices(url, lastDate)

        for price in reversed(res):
            date = price["date"]
            value = price["price"]
            print "Add new price..."
            sql = "insert into sealed_products_price_history (sealed_product_id, date, price) values (%s, %s, %s);"
            sql_values = [sealed_id, date, value]
            cursor = db.cursor()
            cursor.execute(sql, sql_values)
            if commit:
                db.commit()

    print "Over"
    browser.close()
    browser.quit()
