import argparse
import json
import mysql.connector
import re
import urllib2

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="add a Magic The Gathering set to the database using as a source scryfall.")
    parser.add_argument('-s', '--set-code', dest="set_code", help="Set code of the set to add to the database.")
    parser.add_argument('-l', '--lang', dest="lang", default="en", help="Language code of the set. Default is english. Codes are en, ja, fr.")
    parser.add_argument('-c', '--commit', dest="commit", action="store_true", default=False, help="Commit to the database.")
    # parser.add_argument('-f', '--fields', dest="fields", default="", help="List of field to update, separated by semi-colon [image_url].")
    options = parser.parse_args()

    COMMIT = options.commit
    SET_CODE = options.set_code
    LANG = options.lang
    #FIELDS = options.fields.split(';')
    #ADD = len(FIELDS) > 0
    USE_SCRYFALL = True

    connection = mysql.connector.connect(host="localhost", user="root", database="wallstreet")

    if USE_SCRYFALL:
        #get the set information from scryfall
        set_url = "https://api.scryfall.com/sets/" + SET_CODE
        req = urllib2.Request(set_url)
        response = urllib2.urlopen(req)
        text = response.read()
    else:
        set_filepath = "C:\\card\\scryfall\\set_" + SET_CODE + ".json"
        with open(set_filepath, 'r') as f:
            text = f.read()

    setData = json.loads(text)

    # check first if the set exists
    sql = "select id from sets where code = %s"
    sqlValues = [SET_CODE]
    cursor = connection.cursor()
    cursor.execute(sql, sqlValues)
    results = cursor.fetchall()
    if len(results) > 0:
        set_id = results[0][0]
        print("The set %s already exist in the table sets", SET_CODE)
    else:
        insertSetSql = "insert into sets (name, code, release_date, game_id) values (%s, %s, %s, 1)"
        sqlValues = [setData["name"], setData["code"], setData["released_at"] + " 00:00:00"]
        cursor = connection.cursor()
        cursor.execute(insertSetSql, sqlValues)

        if COMMIT:
            connection.commit()

        set_id = cursor.lastrowid

    # find the language id
    sql = "select id from languages where code = %s"
    sqlValues = [LANG]
    cursor = connection.cursor()
    cursor.execute(sql, sqlValues)
    results = cursor.fetchall()
    lang_id = 0
    if len(results) > 0:
        lang_id = results[0][0]
        print "Language %s found with id %s" % (LANG, lang_id)
    else:
        print("ERROR: the language with code %s doesn't exist.", LANG)
        exit(1)

    # check if the set_lang exist
    sql = "select id from sets_langs where sets_langs.set_id = %s and sets_langs.lang_id = %s"
    sqlValues = [set_id, lang_id]
    cursor = connection.cursor()
    cursor.execute(sql, sqlValues)
    results = cursor.fetchall()
    if len(results) > 0:
        set_lang_id = results[0][0]
        print("The set_lang %s %s already exist in the table sets", SET_CODE, LANG)
    else:
        sql = "insert into sets_langs (set_id, lang_id, name, release_date) values (%s, %s, %s, %s)"
        sqlValues = [set_id, lang_id, setData["name"], setData["released_at"]]
        cursor = connection.cursor()
        cursor.execute(sql, sqlValues)

        if COMMIT:
            connection.commit()

        set_lang_id = cursor.lastrowid
        print "Set %s %s added to sets_langs" % (SET_CODE, LANG)

    #get the card information from scryfall
    card_list_url_pattern = "https://api.scryfall.com/cards/search?order=set&q=e%3A{}+lang%3A{}&unique=prints"
    card_list_url = card_list_url_pattern.format(SET_CODE, LANG)
    hasMore = True
    index = 0
    cardAdded = 0
    while hasMore:

        if USE_SCRYFALL:
            req = urllib2.Request(card_list_url)
            response = urllib2.urlopen(req, timeout=500)
            text = response.read()
        else:
            set_filepath = "C:\\card\\scryfall\\cards_" + SET_CODE + "_" + str(index) + ".json"
            with open(set_filepath, 'r') as f:
                text = f.read()

        cardList = json.loads(text)

        data = cardList["data"]
        for card in data:
            image_url = card["image_uris"]["normal"]
            number = card["collector_number"]
            variation = None

            isVariation = not number.isdigit()
            if isVariation:
                splitted = re.split("([0-9]*)([a-zA-Z])", number)
                number = splitted[1]
                variation = splitted[2]

            tcgPlayerUrl = None
            if "purchase_uris" in card:
                if "tcgplayer" in card["purchase_uris"]:
                    tcgPlayerUrl = card["purchase_uris"]["tcgplayer"]

            cardInsertSql = "insert into card (name, set_lang_id, rarity, variation, tcg_url, display_number, image_url, printed_number) values (%s, %s, %s, %s, %s, %s, %s, %s)"

            card_name = card["name"]
            if "printed_name" in card:
                card_name = card["printed_name"]

            cardInsertSqlValues = [card_name, set_lang_id, card["rarity"], variation, tcgPlayerUrl, int(number), image_url, number]
            cursor = connection.cursor()
            cursor.execute(cardInsertSql, cardInsertSqlValues)
            if COMMIT:
                connection.commit()

            cardAdded = cardAdded + 1
            print "Card added : %s" % str(cardAdded)

        index = index + 1
        hasMore = cardList["has_more"]
        if hasMore:
            card_list_url = cardList["next_page"]

    print "Over"
