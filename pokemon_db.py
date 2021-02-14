
from selenium import webdriver
import lxml.html

print "Setup webdriver..."
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--start-maximized")
browser = webdriver.Chrome(executable_path="c:\\workspace\\python\\chromedriver.exe", chrome_options=chromeOptions)


def get_card_information(url):
    global browser
    browser.get(url)

    text_html = browser.execute_script("return document.body.innerHTML")
    html = lxml.html.fromstring(text_html)

    entry = {}

    xpath_card_name = "//h1[contains(@class, 'product-details__name')]"
    element = html.xpath(xpath_card_name)
    entry["name"] = element[0].text

    xpath_set_name = "//div[contains(@class, 'product-details__set')]/a"
    element = html.xpath(xpath_set_name)
    set_name = element[0].text
    set_name = set_name.strip('\n').strip()
    entry["set_name"] = set_name

    xpath_number_rarity = "//dl[contains(@class, 'product-description')]/dd"
    element = html.xpath(xpath_number_rarity)
    raw_text = element[0].text
    splitted_raw_text = raw_text.split('/')
    entry["number"] = int(splitted_raw_text[0])
    entry["rarity"] = splitted_raw_text[1].strip()

    entry["tcg_url"] = url
    return entry


def write_entry_to_db(csv_filname, entry):
    new_line = "{};{};{};{};{};Unlimited\n"
    new_line = new_line.format(entry["set_name"], entry["name"], entry["number"], entry["rarity"], entry["tcg_url"])
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
    entry = get_card_information(url)

    print str(entry)
    csv_filename = "C:\\workspace\\python\\pokemon_urls\\db.csv"

    print "writing to csv..."
    write_entry_to_db(csv_filename, entry)

browser.close()
