import csv
import logging
import lxml.html
import mysql.connector
import os
import re
import sys
import time
import uuid

from selenium import webdriver

sys.path.append("../")
from db.db_csv import DbCsv
from db.entry import Entry

GAMENAME = "Pokemon"

logging.basicConfig(level=logging.INFO)
rootLogger = logging.getLogger()

logFilename = "c:/tmp/log_%s_%d.log" % (__name__, os.getpid())
fileHandler = logging.FileHandler(logFilename)
rootLogger.addHandler(fileHandler)

log = logging.getLogger(__name__)


class DbPokemon(DbCsv):
    m_browser = None
    m_csvFilename = ""

    def __init__(self, browser, csv_filename):
        self.m_browser = browser
        self.m_csvFilename = csv_filename

    def scrap_card_information(self, _url, set_code):
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
        set_clean_name = element[0].text
        set_clean_name = set_clean_name.strip('\n').strip()
        newEntry.set_name = set_clean_name
        newEntry.set_code = set_code

        xpath_number = "//li/strong[contains(text(), \"Card Number / Rarity:\")]/following-sibling::span"
        elements = html.xpath(xpath_number)

        number_element = elements[0]
        number_rarity = number_element.text
        splitted = number_rarity.split("/")
        if len(splitted) == 2:      # pattern is : 55 / Common
            newEntry.number = splitted[0].strip()
            newEntry.rarity = splitted[1].strip()
        elif len(splitted) == 3:
            pattern = "(\D)"
            matches = re.match(pattern, splitted[0].strip())
            if matches is None: # pattern is : 15/115 / Common
                newEntry.number = splitted[0].strip()
                newEntry.rarity = splitted[2].strip()
            else:       # pattern is : Q/115 / Common
                newEntry.number = splitted[0].strip() + splitted[1].strip()
                newEntry.rarity = splitted[2].strip()

        newEntry.id = uuid.uuid4().int
        newEntry.tcg_url = _url
        newEntry.variation = "None"
        log.info("Found card %s", newEntry.name)
        return newEntry

    def write(self, _entry):
        new_line = "{};\"{}\";\"{}\";\"{}\";{};{};{};{}\n"
        new_line = new_line.format(_entry.id, _entry.set_name, _entry.set_code, _entry.name, _entry.number, _entry.rarity, _entry.tcg_url, _entry.variation)
        with open(self.m_csvFilename, "a") as f:
            f.write(new_line)

    def load(self):
        entries = []
        with open(self.m_csvFilename) as csvFile:
            lines = csv.reader(csvFile, delimiter=';', quotechar='"')
            for line in lines:
                newEntry = Entry()
                if len(line) == 0:  # empty line
                    continue
                newEntry.id = line[0]
                newEntry.set_name = line[1]
                newEntry.set_code = line[2]
                newEntry.name = line[3]
                newEntry.number = line[4]
                newEntry.rarity = line[5]
                newEntry.tcg_url = line[6]
                newEntry.variation = line[7]
                if len(line) > 8 and line[8] == '1':
                    newEntry.own = True
                else:
                    newEntry.own = False
                entries.append(newEntry)

        return entries


def scrap_all(set_input, csv_filename):
    log.info("Setup webdriver...")
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--start-maximized")
    browser = webdriver.Chrome(executable_path="C:/workspace/python/chromedriver.exe", chrome_options=chromeOptions)

    filename = csv_filename
    db = DbPokemon(browser, filename)

    search_url_pattern = set_input["url"]

    page_count = set_input["page_count"]
    for page_id in range(1, page_count + 1):
        log.info("Scrap page %d of %d...", page_id, page_count)
        complete_search_url = search_url_pattern.format(page_id)

        browser.get(complete_search_url)
        time.sleep(2)
        text_html = browser.execute_script("return document.body.innerHTML")
        html = lxml.html.fromstring(text_html)

        xpath_cards = "//div[contains(@class, 'search-result__content')]/a"
        elements = html.xpath(xpath_cards)

        for element in elements:
            card_url = element.attrib.get('href')
            card_url = "http://tcgplayer.com" + card_url

            log.info(card_url + "...")
            entry = db.scrap_card_information(card_url, set_input["code"])

            log.info("writing to csv...")
            db.write(entry)

    browser.close()


def load_csv(csv_filename):
    db = DbPokemon(None, csv_filename)
    entries = db.load()
    return entries


# Push a set to the db and return its id
def push_set_to_db(set_index, commit):
    connection = mysql.connector.connect(host="localhost", user="root", database="wallstreet")

    # find the game id
    sql = "select id from game where game.name=%s"
    sql_values = [GAMENAME]
    cursor = connection.cursor()
    cursor.execute(sql, sql_values)
    results = cursor.fetchall()
    if len(results) != 1:
        print ("Error : Failed to find Pokemon in the game table")
        return

    game_id = results[0][0]

    set_info = sets[set_index]

    #check if the set is already there
    sql = "select id from sets where sets.name=%s and sets.game_id=%s"
    sql_values = [set_info["clean_name"], game_id]
    cursor = connection.cursor()
    cursor.execute(sql, sql_values)
    results = cursor.fetchall()
    if len(results) > 0:
        return results[0][0]  # the set already exists in the db

    # add the set
    sql = "insert into sets (name, code, release_date, game_id) values (%s, %s, %s, %s)"
    sql_values = [set_info["clean_name"], set_info["code"], set_info["release_date"], game_id]
    cursor = connection.cursor()
    cursor.execute(sql, sql_values)
    if commit:
        connection.commit()

    return cursor.lastrowid


# Push all entries to the cards table
def push_to_db(entries, set_id, variation, commit):
    connection = mysql.connector.connect(host="localhost", user="root", database="wallstreet")
    for card in entries:
        cardInsertSql = "insert into card (name, set_id, rarity, variation, tcg_url, number) values (%s, %s, %s, %s, %s, %s)"

        # extract the card number from the fftcg number which is <opus>-<number><rarity>
        pattern = "\\d*-(\\d*)."
        matches = re.match(pattern, card.number)
        number = matches.group(1)
        cardInsertSqlValues = [card.name, set_id, card.rarity, variation, card.tcg_url, int(number)]
        cursor = connection.cursor()

        # If the commit flag is false then we didn't push the set so the set_id doesn't exist.
        # Executing the request will trigger a foreign key execption.
        if commit:
            cursor.execute(cardInsertSql, cardInsertSqlValues)
            connection.commit()


if __name__ == "__main__":
    log.info("Setup webdriver...")
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--start-maximized")
    browser = webdriver.Chrome(executable_path="C:/workspace/python/chromedriver.exe", chrome_options=chromeOptions)

    filename = "C:\\workspace\\python\\data\\pokemon\\db_unseen-forces.csv"
    db = DbPokemon(browser, filename)

    url = "https://www.tcgplayer.com/product/90184/pokemon-unseen-forces-unown-q/before?xid=pi676a6c30-2663-4a95-8439-59e6360f8f2e&page=1&Language=English"
    #url = "http://tcgplayer.com/product/85081/pokemon-unseen-forces-eevee?xid=pi3376190c-4835-4350-a9dd-14f41d33484d&page=1"
    entry = db.scrap_card_information(url, "uf")

    log.info("Over")
