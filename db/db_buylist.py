import mysql.connector
from db.entry import Entry


def load_buylist(buylist_id):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="wallstreet"
    )

    sql = "select card.id, card.name, sets.name as set_name, sets.code, card.printed_number, card.rarity, card.tcg_url, card.variation " \
          "from buy_list inner join buy_list_card on buy_list.id = buy_list_card.buy_list_id " \
          "inner join card on card.id = buy_list_card.card_id " \
          "inner join sets_langs on card.set_lang_id = sets_langs.id " \
          "inner join sets on sets_langs.set_id=sets.id " \
          "where buy_list.id=" + str(buylist_id)

    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()

    cards = []
    for result in results:
        new_card = Entry()
        new_card.id = result[0]
        new_card.name = result[1]
        new_card.set_name = result[2]
        new_card.set_code = result[3]
        new_card.number = result[4]
        new_card.rarity = result[5]
        new_card.tcg_url = result[6]
        new_card.variation = result[7]
        new_card.own = False
        cards.append(new_card)

    return cards

