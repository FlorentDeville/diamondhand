import time
import lxml.html
import re
import uuid

from db.db_csv import DbCsv
from db.entry import Entry

class DbSve(DbCsv):
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
        
        set_code_upper = set_code.upper()
        regex = "(.*) - " + set_code_upper + "(.*)"
        match = re.search(regex, newEntry.name)
        newEntry.name = match.group(1)
        
        #xpath_set_name = "//a[contains(@class, 'product-details__set-name')]/h2"
        xpath_set_name = "//div[contains(@class, 'product-details__name__sub-header__links')]/div/a/span"
        element = html.xpath(xpath_set_name)
        set_clean_name = element[0].text
        set_clean_name = set_clean_name.strip('\n').strip()
        newEntry.set_name = set_clean_name
        newEntry.set_code = set_code

        #xpath_number_and_rarity = "//ul[contains(@class, \"product__item-details__attributes\")]/li/span"
        xpath_number_and_rarity = "//ul[contains(@class, \"product__item-details__attributes\")]/li/div/span"
        elements = html.xpath(xpath_number_and_rarity)
        newEntry.rarity = elements[0].text
        newEntry.number = elements[1].text
        #splitted = number_and_rarity.split(" - ")

        #newEntry.number = splitted[0].strip()
        #newEntry.rarity = splitted[1].strip()
        
        newEntry.id = uuid.uuid4().int
        newEntry.tcg_url = _url
        newEntry.variation = "None"
        return newEntry
