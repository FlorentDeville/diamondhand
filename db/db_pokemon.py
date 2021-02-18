import uuid

from selenium import webdriver
import lxml.html

from db.db_csv import DbCsv
from db.entry import Entry

#print "Setup webdriver..."
#chromeOptions = webdriver.ChromeOptions()
#chromeOptions.add_argument("--start-maximized")
#browser = webdriver.Chrome(executable_path="/chromedriver.exe", chrome_options=chromeOptions)


class DbPokemon(DbCsv):
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
        newEntry.set_code = "bas"  # make a global map of set name to set code

        xpath_number_rarity = "//dl[contains(@class, 'product-description')]/dd"
        element = html.xpath(xpath_number_rarity)
        raw_text = element[0].text
        splitted_raw_text = raw_text.split('/')
        newEntry.number = int(splitted_raw_text[0])
        newEntry.rarity = splitted_raw_text[1].strip()

        newEntry.id = uuid.uuid4().int
        newEntry.tcg_url = _url

        return newEntry

    def write(self, _entry):
        new_line = "{};{};{};{};{};{};Unlimited\n"
        #new_line = new_line.format(entry["set_name"], entry["name"], entry["number"], entry["rarity"], entry["tcg_url"])
        new_line = new_line.format(_entry.id, _entry.set)
        with open(csv_filename, "a") as f:
            f.write(new_line)


url_array = [
    "https://shop.tcgplayer.com/pokemon/base-set/double-colorless-energy",
    "https://shop.tcgplayer.com/pokemon/base-set/fighting-energy",
    "https://shop.tcgplayer.com/pokemon/base-set/fire-energy",
    "https://shop.tcgplayer.com/pokemon/base-set/grass-energy",
    "https://shop.tcgplayer.com/pokemon/base-set/lightning-energy",
    "https://shop.tcgplayer.com/pokemon/base-set/psychic-energy",
    "https://shop.tcgplayer.com/pokemon/base-set/water-energy",
]

for url in url_array:
    print url + "..."
    entry = scrap_card_information(url)

    print str(entry)
    csv_filename = "/pokemon_urls/db.csv"

    print "writing to csv..."
    write_entry_to_db(csv_filename, entry)

browser.close()
