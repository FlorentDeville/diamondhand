import argparse
import csv
import lxml.html
import mysql.connector
import sys
import time
import uuid

from db.db_csv import DbCsv
from db.entry import Entry
from selenium import webdriver

DB_TO_TCG_SET_NAME = {}
DB_TO_TCG_SET_NAME["Base Set"] = "base-set"


class DbPokemon(DbCsv):
    m_browser = None
    m_csv_filename = ""

    def __init__(self, browser, csv_filename):
        self.m_browser = browser
        self.m_csv_filename = csv_filename

    def scrap_card_information(self, _url):
        self.m_browser.get(_url)
        time.sleep(2)
        text_html = self.m_browser.execute_script("return document.body.innerHTML")
        html = lxml.html.fromstring(text_html)

        newEntry = Entry()

        xpath_card_name = "//h1[contains(@class, 'product-details__name')]"
        element = html.xpath(xpath_card_name)
        newEntry.name = element[0].text.strip()

        xpath_set_name = "//h2[contains(@data-testid, 'lblProductDetailsSetName')]"
        element = html.xpath(xpath_set_name)
        set_name = element[0].text
        set_name = set_name.strip('\n').strip()
        newEntry.set_name = set_name
        newEntry.set_code = "i"  # make a global map of set name to set code

        xpath_number_rarity = "//ul[contains(@class, 'product-details')]/li/span"
        elements = html.xpath(xpath_number_rarity)

        raw_text = elements[0].text

        splitted = raw_text.split('/')
        newEntry.number = splitted[0].strip()
        newEntry.rarity = splitted[1].strip()

        newEntry.id = uuid.uuid4().int
        newEntry.tcg_url = _url
        newEntry.variation = "Unlimited"

        return newEntry

    def write(self, _entry):
        new_line = "{};{};{};{};{};{};{};{}\n"
        new_line = new_line.format(_entry.id, _entry.set_name, _entry.set_code, _entry.name, _entry.number, _entry.rarity, _entry.tcg_url, _entry.variation)
        with open(self.m_csv_filename, "a") as f:
            f.write(new_line)

    def load(self):
        entries = []
        with open(self.m_csv_filename) as csvFile:
            lines = csv.reader(csvFile, delimiter=';', quotechar='"')
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
                entries.append(newEntry)

        return entries


def scrap_all(setName):
    print "Setup webdriver..."
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--start-maximized")
    browser = webdriver.Chrome(executable_path="C:/workspace/python/chromedriver.exe", chrome_options=chromeOptions)

    search_url_pattern = "https://www.tcgplayer.com/search/pokemon/{}?productLineName=pokemon&setName={}&ProductTypeName=Cards&page="
    tcg_set_name = DB_TO_TCG_SET_NAME[setName]
    search_url = search_url_pattern.format(tcg_set_name, tcg_set_name)

    db = DbPokemon(browser, "C:\\workspace\\python\\pokemon_urls\\db.csv")

    page_count = 10
    cards_collection = []
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

            print entry.to_string()
            cards_collection.append(entry)

    print "Write to csv..."
    for entry in cards_collection:
        db.write(entry)

    print "Over"
    browser.close()


if __name__ == "__main__":
    #parser = argparse.ArgumentParser(description="Parse tcgplayer to create the list of cards in a set of Pokemon.")
    #parser.add_argument('--set-name', '-s', dest="setName", help="Name of the set to work with : Base Set")
    #parser.add_argument("--scrap", dest="scrap", action="store_true", default=False, help="Scrap the data from tcgplayer.")
    #parser.add_argument('--commit', '-c', dest="commit", action="store_true", default=False, help="Commit to the database.")
    #options = parser.parse_args(sys.argv)

    SCRAP = False
    WRITE_IN_DB = True
    COMMIT = True

    if SCRAP is True:
        set_name = "Base Set"
        scrap_all(set_name)
    elif WRITE_IN_DB is True:
        db = DbPokemon(None, "C:\\workspace\\python\\pokemon_urls\\db.csv")
        entries = db.load()

        connection = mysql.connector.connect(host="localhost", user="root", database="wallstreet")

        setId = 23
        for card in entries:
            print card.name + "..."
            cardInsertSql = "insert into card (name, set_id, rarity, variation, tcg_url, number) values (%s, %s, %s, %s, %s, %s)"
            cardInsertSqlValues = [card.name, setId, card.rarity, card.variation, card.tcg_url, int(card.number)]
            cursor = connection.cursor()
            cursor.execute(cardInsertSql, cardInsertSqlValues)
            if COMMIT:
                connection.commit()

    print "Over"
