import argparse
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

GAMENAME = "Final Fantasy"

sets = {}
sets[1] = {}
sets[1]["url"] = "https://www.tcgplayer.com/search/final-fantasy-tcg/opus-i?productLineName=final-fantasy-tcg&view=grid&page={}&setName=opus-i"
sets[1]["name"] = "opus-i"
sets[1]["clean_name"] = "Opus I"
sets[1]["page_count"] = 10
sets[1]["code"] = "op1"
sets[1]["release_date"] = "2016-10-28 12:00:00"

sets[2] = {}
sets[2]["url"] = "https://www.tcgplayer.com/search/final-fantasy-tcg/opus-ii?productLineName=final-fantasy-tcg&view=grid&setName=opus-ii&page={}&ProductTypeName=Final%20Fantasy%20Singles"
sets[2]["name"] = "opus-ii"
sets[2]["clean_name"] = "Opus II"
sets[2]["page_count"] = 7
sets[2]["code"] = "op2"
sets[2]["release_date"] = "2017-03-24 12:00:00"

sets[3] = {}
sets[3]["url"] = "https://www.tcgplayer.com/search/final-fantasy-tcg/opus-iii?productLineName=final-fantasy-tcg&view=grid&page={}&ProductTypeName=Final%20Fantasy%20Singles&setName=opus-iii"
sets[3]["name"] = "opus-iii"
sets[3]["clean_name"] = "Opus III"
sets[3]["page_count"] = 7
sets[3]["code"] = "op3"
sets[3]["release_date"] = "2017-07-21 12:00:00"

sets[4] = {}
sets[4]["url"] = "https://www.tcgplayer.com/search/final-fantasy-tcg/opus-iv?productLineName=final-fantasy-tcg&view=grid&page={}&ProductTypeName=Final%20Fantasy%20Singles&setName=opus-iv"
sets[4]["name"] = "opus-iv"
sets[4]["clean_name"] = "Opus IV"
sets[4]["page_count"] = 7
sets[4]["code"] = "op4"
sets[4]["release_date"] = "2017-12-01 12:00:00"

sets[5] = {}
sets[5]["url"] = "https://www.tcgplayer.com/search/final-fantasy-tcg/opus-v?productLineName=final-fantasy-tcg&view=grid&page={}&ProductTypeName=Final%20Fantasy%20Singles&setName=opus-v"
sets[5]["name"] = "opus-v"
sets[5]["clean_name"] = "Opus V"
sets[5]["page_count"] = 7
sets[5]["code"] = "op5"
sets[5]["release_date"] = "2018-03-23 12:00:00"

logging.basicConfig(level=logging.INFO)
rootLogger = logging.getLogger()

logFilename = "c:/tmp/log_%s_%d.log" % (__name__, os.getpid())
fileHandler = logging.FileHandler(logFilename)
rootLogger.addHandler(fileHandler)

log = logging.getLogger(__name__)


class DbFFTcg(DbCsv):
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

        xpath_set_name = "//a[contains(@class, 'product-details__set-name')]/h2"
        element = html.xpath(xpath_set_name)
        set_clean_name = element[0].text
        set_clean_name = set_clean_name.strip('\n').strip()
        newEntry.set_name = set_clean_name
        newEntry.set_code = set_code

        xpath_rarity = "//li/strong[contains(text(), \"Rarity:\")]/following-sibling::span"
        elements = html.xpath(xpath_rarity)

        rarity_element = elements[0]
        newEntry.rarity = rarity_element.text

        xpath_number = "//li/strong[contains(text(), \"Number:\")]/following-sibling::span"
        elements = html.xpath(xpath_number)

        number_element = elements[0]
        newEntry.number = number_element.text

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


def scrap_all(set_index, csv_filename):
    log.info("Setup webdriver...")
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--start-maximized")
    browser = webdriver.Chrome(executable_path="C:/workspace/python/chromedriver.exe", chrome_options=chromeOptions)

    filename = csv_filename
    db = DbFFTcg(browser, filename)

    search_url_pattern = sets[set_index]["url"]

    page_count = sets[set_index]["page_count"]
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
            entry = db.scrap_card_information(card_url, sets[set_index]["code"])

            log.info("writing to csv...")
            db.write(entry)

    browser.close()


def load_csv(csv_filename):
    db = DbFFTcg(None, csv_filename)
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
        print ("Error : Failed to find Final Fantasy in the game table")
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
        pattern = "\\d-(\\d*)."
        matches = re.match(pattern, card.number)
        number = matches.group(1)
        cardInsertSqlValues = [card.name, set_id, card.rarity, variation, card.tcg_url, int(number)]
        cursor = connection.cursor()
        cursor.execute(cardInsertSql, cardInsertSqlValues)
        if commit:
            connection.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse tcgplayer to create the list of cards in a set of FFTCG.")

    setHelpText = "Index of the set to work with:\n"
    for key in sets.keys():
        setHelpText += " %s : %s," % (key, sets[key]["name"])

    parser.add_argument('--set-id', '-s', dest="set_id", help=setHelpText)
    parser.add_argument("--scrap", dest="scrap", action="store_true", default=False, help="Scrap the data from tcgplayer.")
    parser.add_argument("--push", "-p", dest="push", action="store_true", default=False, help="Push csv file to database.")
    parser.add_argument('--commit', '-c', dest="commit", action="store_true", default=False, help="Commit to the database.")
    options = parser.parse_args()
    log.info("Start...")

    if options.set_id is None:
        log.error("Missing set_id")
        exit(1)

    set_index = int(options.set_id)
    if set_index is None or set_index not in sets:
        log.error("ERROR : Unknown value for set_id")
        exit()

    set_name = sets[set_index]["name"]
    csv_filename = "C:\\workspace\\python\\fftcg\\db_" + set_name + ".csv"

    if options.scrap:
        log.info("Scrap...")
        scrap_all(set_index, csv_filename)

    if options.push:
        log.info("Load csv...")
        entries = load_csv(csv_filename)
        log.info("Push set...")
        set_id = push_set_to_db(set_index, options.commit)
        log.info("Push cards...")
        push_to_db(entries, set_id, None, options.commit)

    log.info("Over")
