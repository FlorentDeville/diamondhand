import json
import mysql.connector
import re
import sys
import urllib2


def print_help():
    print "push_mtg_set: add a Magic The Gathering set to the database using as a source scryfall"
    print "Mandatory argument:"
    print "    --set-code | -s <set-code> : set code of the set to add to the database."
    print "Optional argument:"
    print "    --commit | -c : commit to the database."
    print "    --help | -h : print this help text."


if __name__ == "__main__":

    COMMIT = False
    SET_CODE = ""  # "sta"
    USE_SCRYFALL = True

    # parse command line
    argc = len(sys.argv)
    index = 0
    while index < argc:
        arg = sys.argv[index]
        if arg == "--set-code" or arg == "-s":
            index = index + 1
            if index >= argc:
                print "Missing value for argument " + arg
                exit(1)
            else:
                SET_CODE = sys.argv[index]
        elif arg == "--commit" or arg == "-c":
            COMMIT = True
        elif arg == "--help" or arg == "-h":
            print_help()
            exit(0)

        index = index + 1

    if SET_CODE == "":
        print_help()
        exit(1)
    
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

    #push the set to db
    insertSetSql = "insert into sets (name, code, release_date, game_id) values (%s, %s, %s, 1)"
    sqlValues = [setData["name"], setData["code"], setData["released_at"] + " 00:00:00"]
    cursor = connection.cursor()
    cursor.execute(insertSetSql, sqlValues)

    if COMMIT:
        connection.commit()

    print str(cursor.rowcount) + " row inserted"

    setId = cursor.lastrowid

    #get the card information from scryfall
    card_list_url = setData["search_uri"]
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

            cardInsertSql = "insert into card (name, set_id, rarity, variation, tcg_url, number) values (%s, %s, %s, %s, %s, %s)"
            cardInsertSqlValues = [card["name"], setId, card["rarity"], variation, tcgPlayerUrl, int(number)]
            cursor = connection.cursor()
            cursor.execute(cardInsertSql, cardInsertSqlValues)
            if COMMIT:
                connection.commit()

            cardAdded = cardAdded + 1
            print str(cursor.rowcount) + " row inserted/ total " + str(cardAdded)

        index = index + 1
        hasMore = cardList["has_more"]
        if hasMore:
            card_list_url = cardList["next_page"]


    print "Over"
