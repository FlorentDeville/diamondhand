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
sets[1]["url"] = "https://www.tcgplayer.com/search/final-fantasy-tcg/opus-i?productLineName=final-fantasy-tcg&view=grid&page={}&ProductTypeName=Final%20Fantasy%20Singles&setName=opus-i"
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

sets[6] = {}
sets[6]["url"] = "https://www.tcgplayer.com/search/final-fantasy-tcg/opus-vi?productLineName=final-fantasy-tcg&view=grid&page={}&setName=opus-vi&ProductTypeName=Final%20Fantasy%20Singles"
sets[6]["name"] = "opus-vi"
sets[6]["clean_name"] = "Opus VI"
sets[6]["page_count"] = 6
sets[6]["code"] = "op6"
sets[6]["release_date"] = "2018-07-07 12:00:00"

sets[7] = {}
sets[7]["url"] = "https://www.tcgplayer.com/search/final-fantasy-tcg/opus-vii?productLineName=final-fantasy-tcg&view=grid&page={}&setName=opus-vii&ProductTypeName=Final%20Fantasy%20Singles"
sets[7]["name"] = "opus-vii"
sets[7]["clean_name"] = "Opus VII"
sets[7]["page_count"] = 6
sets[7]["code"] = "op7"
sets[7]["release_date"] = "2018-10-28 12:00:00"

sets[8] = {}
sets[8]["url"] = "https://www.tcgplayer.com/search/final-fantasy-tcg/opus-viii?productLineName=final-fantasy-tcg&view=grid&page={}&setName=opus-viii&ProductTypeName=Final%20Fantasy%20Singles"
sets[8]["name"] = "opus-viii"
sets[8]["clean_name"] = "Opus VIII"
sets[8]["page_count"] = 7
sets[8]["code"] = "op8"
sets[8]["release_date"] = "2019-03-16 12:00:00"

sets[9] = {}
sets[9]["url"] = "https://www.tcgplayer.com/search/final-fantasy-tcg/opus-ix?productLineName=final-fantasy-tcg&view=grid&page={}&setName=opus-ix&ProductTypeName=Final%20Fantasy%20Singles"
sets[9]["name"] = "opus-ix"
sets[9]["clean_name"] = "Opus IX"
sets[9]["page_count"] = 6
sets[9]["code"] = "op9"
sets[9]["release_date"] = "2019-07-19 12:00:00"

sets[10] = {}
sets[10]["url"] = "https://www.tcgplayer.com/search/final-fantasy-tcg/opus-x?productLineName=final-fantasy-tcg&view=grid&page={}&setName=opus-x&ProductTypeName=Final%20Fantasy%20Singles"
sets[10]["name"] = "opus-x"
sets[10]["clean_name"] = "Opus X"
sets[10]["page_count"] = 7
sets[10]["code"] = "op10"
sets[10]["release_date"] = "2019-11-08 12:00:00"

sets[11] = {}
sets[11]["url"] = "https://www.tcgplayer.com/search/final-fantasy-tcg/opus-xi?productLineName=final-fantasy-tcg&view=grid&page={}&setName=opus-xi&ProductTypeName=Final%20Fantasy%20Singles"
sets[11]["name"] = "opus-xi"
sets[11]["clean_name"] = "Opus XI"
sets[11]["page_count"] = 7
sets[11]["code"] = "op11"
sets[11]["release_date"] = "2020-03-27 12:00:00"

sets[12] = {}
sets[12]["url"] = "https://www.tcgplayer.com/search/final-fantasy-tcg/opus-xii?productLineName=final-fantasy-tcg&view=grid&page={}&setName=opus-xii&ProductTypeName=Final%20Fantasy%20Singles"
sets[12]["name"] = "opus-xii"
sets[12]["clean_name"] = "Opus XII"
sets[12]["page_count"] = 7
sets[12]["code"] = "op12"
sets[12]["release_date"] = "2020-11-06 12:00:00"

sets[13] = {}
sets[13]["url"] = "https://www.tcgplayer.com/search/final-fantasy-tcg/opus-xiii-crystal-radiance?productLineName=final-fantasy-tcg&view=grid&page={}&setName=opus-xiii-crystal-radiance&ProductTypeName=Final%20Fantasy%20Singles"
sets[13]["name"] = "opus-xiii"
sets[13]["clean_name"] = "Opus XIII: Crystal Radiance"
sets[13]["page_count"] = 7
sets[13]["code"] = "op13"
sets[13]["release_date"] = "2021-03-26 12:00:00"

sets[14] = {}
sets[14]["url"] = "https://www.tcgplayer.com/search/final-fantasy-tcg/opus-xiv-crystal-abyss?productLineName=final-fantasy-tcg&view=grid&page={}&ProductTypeName=Final%20Fantasy%20Singles&setName=opus-xiv-crystal-abyss"
sets[14]["name"] = "opus-xiv"
sets[14]["clean_name"] = "Opus XIV: Crystal Abyss"
sets[14]["page_count"] = 7
sets[14]["code"] = "op14"
sets[14]["release_date"] = "2021-08-06 12:00:00"


class DbFFTcg(DbCsv):
    m_browser = None
    m_csvFilename = ""

    def __init__(self, browser, csv_filename):
        DbCsv.__init__(self)
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

    def raw_name_to_printed_name(self, entry):
        DbCsv.raw_name_to_printed_name(self, entry) # set default value
        pattern_list = [
            "(.*) \(.*\)",
            "(.*) -"
            ]
        for pattern in pattern_list:
            matches = re.match(pattern, entry.name)
            if matches is not None:
                entry.printed_name = matches.group(1)
                return
