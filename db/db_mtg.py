import time
import lxml.html
import uuid

from db.db_csv import DbCsv
from db.entry import Entry
import re

class DbMtg(DbCsv):
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
        if len(element) != 0:
            newEntry.name = element[0].text.strip()
        else:
            newEntry.name = "__ERROR"

        #xpath_set_name = "//a[contains(@class, 'product-details__set-name')]/h2"
        xpath_set_name = "//div[contains(@class, 'product-details__name__sub-header__links')]/div/a/span"
        element = html.xpath(xpath_set_name)
        
        if len(element) != 0:
            set_clean_name = element[0].text
            set_clean_name = set_clean_name.strip('\n').strip()
            newEntry.set_name = set_clean_name
            newEntry.set_code = set_code

        #xpath_number_and_rarity = "//ul[contains(@class, \"product__item-details__attributes\")]/li/span"
        xpath_rarity = "//ul[contains(@class, \"product__item-details__attributes\")]/li/div/span"
        elements = html.xpath(xpath_rarity)
        
        if len(elements) != 0 :
            newEntry.rarity = elements[0].text


        xpath_number = "//ul[contains(@class, \"product__item-details__attributes\")]/li[position()=2]/div/span"
        elements = html.xpath(xpath_number)
        
        if len(elements) != 0:
            newEntry.number = elements[0].text
        
        newEntry.id = uuid.uuid4().int
        newEntry.tcg_url = _url
        newEntry.variation = "None"
        return newEntry

    @staticmethod
    def condition(entry):
        # 99a
        # 99b
        # conversion : set_number * 1000 + letter
        matches = re.match("(\d*)([a-z]?)", entry.number)
        number = matches.group(1)
        letter = matches.group(2)
        sub_number = 0
        if len(letter) != 0:
            sub_number = ord(letter)
        
        multiplier = 10
        if entry.name.endswith("(Serial Numbered)"):
            multiplier = 1000
        elif entry.rarity == "T":
            multiplier = 1000000
        elif entry.rarity == "S":
            multiplier = 100000000

        value = int(number) * multiplier + sub_number
        
        #if entry.rarity == "T":
        #    print("token ", value)
        #else:
        #    print("regular ", value)
        return value

    @staticmethod
    def sort_entries(entries):
        entries.sort(key=DbMtg.condition)
        return entries