
# Single entry for a card in the db
class Entry:
    def __init__(self):
        pass

    id = 0              # id of the card
    set_name = ""       # full name of the set
    set_code = ""       # code name of the set, usually 3 characters
    name = ""           # full name of the card
    number = 0          # number of the card in the set
    rarity = ""         # rarity of the card
    tcg_url = ""        # url in tcgplayer
    variation = ""      # print variation
    own = False         # do I own this card
