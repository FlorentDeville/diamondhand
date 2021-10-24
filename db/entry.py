
# Single entry for a card in the db
class Entry:
    def __init__(self):
        pass

    id = 0              # id of the card
    set_name = ""       # full name of the set
    set_code = ""       # code name of the set, usually 3 characters
    name = ""           # raw name of the card as scrapped from the website and saved in the csv
    printed_name = ""   # name of the card as printed on the card.
    number = 0          # number of the card in the set
    rarity = ""         # rarity of the card
    tcg_url = ""        # url in tcgplayer
    variation = ""      # print variation
    own = False         # do I own this card

    def to_string(self):
        pattern = "{};{};{};{};{};{};{};{};{}"
        res = pattern.format(self.id, self.set_name, self.set_code, self.name, self.number, self.rarity, self.tcg_url, self.variation, self.own)
        return res
