import uuid

from selenium import webdriver
import csv
import lxml.html
import time

from db.db_csv import DbCsv
from db.entry import Entry


class DbFFTcg(DbCsv):
    m_browser = None
    m_csvFilename = ""

    def __init__(self, browser, csv_filename):
        self.m_browser = browser
        self.m_csvFilename = csv_filename

    def scrap_card_information(self, _url):
        self.m_browser.get(_url)

        text_html = self.m_browser.execute_script("return document.body.innerHTML")
        html = lxml.html.fromstring(text_html)

        newEntry = Entry()

        xpath_card_name = "//h1[contains(@class, 'product-details__name')]"
        element = html.xpath(xpath_card_name)
        newEntry.name = element[0].text

        xpath_set_name = "//div[contains(@class, 'product-details__set')]/a"
        element = html.xpath(xpath_set_name)
        set_name = element[0].text
        set_name = set_name.strip('\n').strip()
        newEntry.set_name = set_name
        newEntry.set_code = "i"  # make a global map of set name to set code

        xpath_number_rarity = "//dl[contains(@class, 'product-description')]/dd"
        elements = html.xpath(xpath_number_rarity)

        rarity_element = elements[0]
        newEntry.rarity = rarity_element.text

        number_element = elements[1]
        newEntry.number = number_element.text

        newEntry.id = uuid.uuid4().int
        newEntry.tcg_url = _url
        newEntry.variation = "None"

        return newEntry

    def write(self, _entry):
        new_line = "{};{};{};{};{};{};{};{}\n"
        new_line = new_line.format(_entry.id, _entry.set_name, _entry.set_code, _entry.name, _entry.number, _entry.rarity, _entry.tcg_url, _entry.variation)
        with open(self.m_csvFilename, "a") as f:
            f.write(new_line)

    def load(self):
        entries = []
        with open(self.m_csvFilename) as csvFile:
            lines = csv.reader(csvFile, delimiter=',', quotechar='"')
            for line in lines:
                newEntry = Entry()
                newEntry.id = line[0]
                newEntry.set_name = line[1]
                newEntry.set_code = line[2]
                newEntry.name = line[3]
                newEntry.number = line[4]
                newEntry.rarity = line[5]
                newEntry.tcg_url = line[6]
                newEntry.variation = line[7]
                if line[8] == '0':
                    newEntry.own = False
                else:
                    newEntry.own = True
                entries.append(newEntry)

        return entries


def scrap_all():
    print "Setup webdriver..."
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--start-maximized")
    browser = webdriver.Chrome(executable_path="C:/workspace/python/chromedriver.exe", chrome_options=chromeOptions)

    db = DbFFTcg(browser, "C:\\workspace\\python\\fftcg\\db.csv")

    search_url = "https://www.tcgplayer.com/search/final-fantasy-tcg/opus-i?productLineName=final-fantasy-tcg&setName=opus-i&ProductTypeName=Final%20Fantasy%20Singles&page="
    page_count = 10

    for page_id in range(1, page_count+1):
        print "Scrap page " + str(page_id) + " of " + str(page_count) + "..."
        complete_search_url = search_url + str(page_id)

        browser.get(complete_search_url)
        time.sleep(2)
        text_html = browser.execute_script("return document.body.innerHTML")
        html = lxml.html.fromstring(text_html)

        xpath_cards = "//a[contains(@class, 'search-result__product')]"
        elements = html.xpath(xpath_cards)

        for element in elements:
            card_url = element.attrib.get('href')

            print card_url + "..."
            entry = db.scrap_card_information(card_url)

            print "writing to csv..."
            db.write(entry)

    print "Over"
    browser.close()


def load_csv():
    print "Setup webdriver..."
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--start-maximized")
    browser = webdriver.Chrome(executable_path="C:/workspace/python/chromedriver.exe", chrome_options=chromeOptions)

    db = DbFFTcg(browser, "C:\\workspace\\python\\fftcg\\db.csv")
    entries = db.load()

    browser.close()


if __name__ == "__main__":
    load_csv()
