import time
import lxml.html
import uuid

from db.db_csv import DbCsv
from db.entry import Entry

class DbDbs(DbCsv):
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

       # xpath_card_name = "//h1[contains(@class, 'product-details__name')]"
        xpath_card_name = "//span[contains(@class, 'lastcrumb')]"
        element = html.xpath(xpath_card_name)
        newEntry.name = element[0].text.strip()

        #xpath_set_name = "//a[contains(@class, 'product-details__set-name')]/h2"
        xpath_set_name = "//div[contains(@class, 'product-details__name__sub-header__links')]/div/a/span"
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

    @staticmethod
    def condition(entry):
        return entry.number

    @staticmethod
    def sort_entries(entries):
        # Make a group of no variation and a group of foil
        no_variation = [card for card in entries if card.variation == "None"]
        foil = [card for card in entries if card.variation == "Foil"]

        no_variation.sort(key=DbDbs.condition)
        foil.sort(key=DbDbs.condition)

        no_variation.extend(foil)

        return no_variation
