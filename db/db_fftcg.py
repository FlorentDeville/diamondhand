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

class DbFFTcg(DbCsv):
    m_browser = None
    m_csvFilename = ""

    def __init__(self, browser, csv_filename):
        DbCsv.__init__(self)
        self.m_browser = browser
        self.m_csvFilename = csv_filename

    def scrap_card_information(self, _url, set_code):
        self.m_browser.get(_url)
        time.sleep(4)
        text_html = self.m_browser.execute_script("return document.body.innerHTML")
        html = lxml.html.fromstring(text_html)

        newEntry = Entry()

        xpath_card_name = "//h1[contains(@class, 'product-details__name')]"
       # xpath_card_name = "//span[contains(@class, 'lastcrumb')]"
        element = html.xpath(xpath_card_name)
        newEntry.name = element[0].text.strip()

        #xpath_set_name = "//a[contains(@class, 'product-details__set-name')]/h2"
        xpath_set_name = "//div[contains(@class, 'product-details__name__sub-header__links')]/div/a/span"
        element = html.xpath(xpath_set_name)
        set_clean_name = element[0].text
        set_clean_name = set_clean_name.strip('\n').strip()
        newEntry.set_name = set_clean_name
        newEntry.set_code = set_code

        xpath_rarity = "//li/div/strong[contains(text(), \"Rarity:\")]/following-sibling::span"
        elements = html.xpath(xpath_rarity)

        rarity_element = elements[0]
        newEntry.rarity = rarity_element.text

        xpath_number = "//li/div/strong[contains(text(), \"Number:\")]/following-sibling::span"
        elements = html.xpath(xpath_number)

        number_element = elements[0]
        newEntry.number = number_element.text

        newEntry.id = uuid.uuid4().int
        newEntry.tcg_url = _url
        newEntry.variation = "None"
        return newEntry

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

    @staticmethod
    def condition(entry):
        # 12-100L
        # C-004
        # conversion : set_number * 1000 + card_number
        # if set_number is a string : set_number * 100000 + card_number
        matches = re.match("(.*)-(\d*)(\D)?", entry.number)
        set_number = matches.group(1)
        card_number = matches.group(2)

        if set_number.isdigit():
            return int(set_number) * 1000 + int(card_number)
        else:
            return ord(set_number) * 100000 + int(card_number)

    @staticmethod
    def sort_entries(entries):
        # first split the cards by group: no variation, full art and full art reprint
        no_variation = [card for card in entries if card.variation == "None"]
        full_art = [card for card in entries if card.variation == "Full Art"]
        reprint = [card for card in entries if card.variation == "Full Art Reprint"]

        no_variation.sort(key=DbFFTcg.condition)
        full_art.sort(key=DbFFTcg.condition)
        reprint.sort(key=DbFFTcg.condition)

        no_variation.extend(full_art)
        no_variation.extend(reprint)

        return no_variation
