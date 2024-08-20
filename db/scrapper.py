import argparse

import json
import logging
import lxml.html
import os
import sys
import time

from argparse import RawTextHelpFormatter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

sys.path.append("../")
from db.connection import get_connection
from db.scrapper_images import scrap_images
from db.db_cfv import DbCfv
from db.db_fftcg import DbFFTcg
from db.db_dbs import DbDbs
from db.db_mtg import DbMtg
from db.db_op import DbOp
from db.db_pokemon import DbPokemon

from db.helper_pokemon import *

logging.basicConfig(level=logging.INFO)
rootLogger = logging.getLogger()

logFilename = "c:/tmp/log_%s_%d.log" % (__name__, os.getpid())
fileHandler = logging.FileHandler(logFilename)
rootLogger.addHandler(fileHandler)

log = logging.getLogger(__name__)


def scrap_all(game_name, set, csv_filename):
    log.info("Setup webdriver...")
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--start-maximized")

    service = Service(executable_path="C:/workspace/DiamondHand/chromedriver.exe")
    browser = webdriver.Chrome(service=service, options=chromeOptions)

    filename = csv_filename
    db = None
    if game_name == "pokemon":
        db = DbPokemon(browser, filename)
    elif game_name == "fftcg":
        db = DbFFTcg(browser, filename)
    elif game_name == "dbs":
        db = DbDbs(browser, filename)
    elif game_name == "op":
        db = DbOp(browser, filename)
    elif game_name == "cfv":
        db = DbCfv(browser, filename)
    elif game_name == "mtg":
        db = DbMtg(browser, filename)
    else:
        log.exception("Unknown game %s", game_name)
        exit(1)

    search_url_pattern = set["url"]

    page_count = set["page_count"]
    for page_id in range(1, page_count + 1):
        log.info("Scrap page %d of %d...", page_id, page_count)
        complete_search_url = search_url_pattern.format(page_id)

        browser.get(complete_search_url)
        TIME_TO_WAIT = 4
        time.sleep(TIME_TO_WAIT)
        text_html = browser.execute_script("return document.body.innerHTML")
        html = lxml.html.fromstring(text_html)

        xpath_cards = "//div[contains(@class, 'product-card__content')]/a"
        elements = html.xpath(xpath_cards)

        for element in elements:
            card_url = element.attrib.get('href')
            card_url = "http://tcgplayer.com" + card_url

            log.info(card_url + "...")
            entry = db.scrap_card_information(card_url, set["code"])
            if entry is None:
                log.info("ignoring card")
                continue

            log.info("writing to csv...")
            db.write(entry)

    browser.close()


def load_csv(csv_filename):
    db = DbFFTcg(None, csv_filename)
    entries = db.load()
    return entries


# Push a set to the db and return its id
def push_set_to_db(selected_game, selected_set, selected_lang, commit, connection_name):
    connection = get_connection(connection_name)

    # find the game id
    sql = "select id from game where game.name=%s"
    sql_values = [selected_game["clean_name"]]
    cursor = connection.cursor()
    cursor.execute(sql, sql_values)
    results = cursor.fetchall()
    if len(results) != 1:
        print ("Error : Failed to find Final Fantasy in the game table")
        return

    game_id = results[0][0]

    #check if the set is already there
    sql = "select id from sets where sets.name=%s and sets.game_id=%s"
    sql_values = [selected_set["clean_name"], game_id]
    cursor = connection.cursor()
    cursor.execute(sql, sql_values)
    results = cursor.fetchall()
    set_id = -1
    if len(results) > 0:
        set_id = results[0][0]  # the set already exists in the db
    else:
        # add the set
        sql = "insert into sets (name, code, release_date, game_id) values (%s, %s, %s, %s)"
        sql_values = [selected_set["clean_name"], selected_set["code"], selected_set["release_date"], game_id]
        cursor = connection.cursor()
        cursor.execute(sql, sql_values)
        if commit:
            connection.commit()

        set_id = cursor.lastrowid

    # get the lang id
    sql = "select id from languages where code = %s"
    sql_values=[selected_lang]
    cursor = connection.cursor()
    cursor.execute(sql, sql_values)
    results = cursor.fetchall()
    lang_id = -1
    if len(results) > 0:
        lang_id = results[0][0]
    else:
        log.exception("Unknown language %s", selected_lang)

    # check if the set_lang is there
    sql = "select id from sets_langs where set_id = %s and lang_id = %s"
    sql_values = [set_id, lang_id]
    cursor = connection.cursor()
    cursor.execute(sql, sql_values)
    results = cursor.fetchall()
    set_lang_id = -1
    if len(results) > 0:
        set_lang_id = results[0][0]  # the set already exists in the db
    else:
        # add the set_lang
        sql = "insert into sets_langs (set_id, lang_id, name, release_date) values (%s, %s, %s, %s)"
        sql_values = [set_id, lang_id, selected_set["clean_name"], selected_set["release_date"]]
        cursor = connection.cursor()
        cursor.execute(sql, sql_values)
        if commit:
            connection.commit()

        set_lang_id = cursor.lastrowid

    return set_lang_id


# Push all entries to the cards table
def push_to_db(entries, selected_game, set_lang_id, commit, connection_name):
    if selected_game["name"] == "pokemon":
        helper_pokemon_sort_cards(entries)
    elif selected_game["name"] == "fftcg":
        entries = DbFFTcg.sort_entries(entries)
    elif selected_game["name"] == "dbs":
        entries = DbDbs.sort_entries(entries)
    else:
        log.warn("No sort code for game %s. Use default sort.", selected_game["name"])
        entries.sort(key=lambda x: x.number)

    connection = get_connection(connection_name)

    for ii in range(len(entries)):
        card = entries[ii]

        cardInsertSql = "insert into card (name, set_lang_id, rarity, variation, tcg_url, display_number, printed_number) values (%s, %s, %s, %s, %s, %s, %s)"

        card_name = card.name
        printed_number = card.number
        display_number = ii
        variation = None

        if card.variation is not None:
            variation = card.variation    

        if selected_game["name"] == "pokemon":
            card_name = helper_pokemon_get_name(card)

        cardInsertSqlValues = [card_name, set_lang_id, card.rarity, variation, card.tcg_url, display_number, printed_number]
        cursor = connection.cursor()
        cursor.execute(cardInsertSql, cardInsertSqlValues)

        # If the commit flag is false then we didn't push the set so the set_id doesn't exist.
        # Executing the request will trigger a foreign key execption.
        if commit:
            connection.commit()


def delete_cards_from_set_lang(set_lang_id, commit, connection_name):
    connection = get_connection(connection_name)
    sql = "delete from card where set_lang_id = %s"
    sql_values = [set_lang_id]
    cursor = connection.cursor()
    cursor.execute(sql, sql_values)
    if commit:
        connection.commit()


def make_csv_filename(game_name, set_code):
    csv_filename = "C:\\workspace\\DiamondHand\\data\\%s\\db_%s.csv" % (game_name, set_code)
    return csv_filename


if __name__ == "__main__":

    # load games definition
    current_dir = os.path.dirname(os.path.abspath(__file__))
    games_json_file = os.path.join(current_dir, "input_games.json")
    with open(games_json_file, "r") as f:
        games_list = json.loads(f.read())

    # load all sets
    sets_list = {}
    for game in games_list:
        json_filename = "input_%s.json" % (game["name"])
        json_file = os.path.join(current_dir, json_filename)
        with open(json_file, "r") as f:
            sets = json.loads(f.read())

        sets_list[game["name"]] = sets

    parser = argparse.ArgumentParser(description="Parse tcgplayer to create the list of cards in a set.", formatter_class=RawTextHelpFormatter)

    game_help_text = "Index of games:\n"
    for game in games_list:
        game_help_text += "\t%s\n" % (game["name"])

    parser.add_argument('--game', '-g', dest="game", help=game_help_text)
    parser.add_argument('--setlist', dest="list_sets", action="store_true", default=False, help="List the sets for the selected game")
    parser.add_argument('--set-id', '-s', dest="set_id", help="Index of the set to work with")
    parser.add_argument("--scrap", dest="scrap", action="store_true", default=False, help="Scrap the data from tcgplayer.")
    parser.add_argument("--scrap-image", dest="scrap_image", action="store_true", default=False, help="Scrap image data from tcgplayer.")
    parser.add_argument("--push", "-p", dest="push", action="store_true", default=False, help="Push csv file to database.")
    parser.add_argument('--commit', '-c', dest="commit", action="store_true", default=False, help="Commit to the database.")
    parser.add_argument('--online', '-o', dest="online", action="store_true", default=False, help="Push to the online db. By default, push to the local db.")
    parser.add_argument('--broadcast', '-b', dest="broadcast", action="store_true", default=False, help="Push to the local and  online db. By default, push only to the local db.")
    parser.add_argument('--test-connection', '-t', dest="test_connection", action="store_true", default=False, help="Test the mysql connection.")
    parser.add_argument('--clean-cards', dest="clean_cards", action="store_true", default=False, help="Delete all the existing cards for the set before pushing again")
    options = parser.parse_args()
    log.info("Start...")

    if options.list_sets:
        if options.game is None:
            log.error("Missing -g argument")
            exit(1)

        sets = sets_list[options.game]
        for index in range(len(sets)):
            log.info("%d : %s (%s)", index, sets[index]["clean_name"], sets[index]["code"])

        exit()

    if options.scrap:
        if options.game is None:
            log.error("Missing argument --game")
            exit(1)

        if options.set_id is None:
            log.error("Missing argument --set_id")
            exit(1)

        selected_game = None
        for game in games_list:
            if game["name"] == options.game:
                selected_game = game

        if selected_game is None:
            log.error("Unknown game %s", options.game)
            exit(1)

        selected_set = sets_list[selected_game["name"]][int(options.set_id)]

        log.info("Scrap %s %s...", selected_game["clean_name"], selected_set["clean_name"])
        csv_filename = make_csv_filename(selected_game["name"], selected_set["code"])
        scrap_all(selected_game["name"], selected_set, csv_filename)

    if options.scrap_image:
        if options.game is None:
            log.error("Missing argument --game")
            exit(1)

        if options.set_id is None:
            log.error("Missing argument --set_id")
            exit(1)

        selected_game = None
        for game in games_list:
            if game["name"] == options.game:
                selected_game = game

        if selected_game is None:
            log.error("Unknown game %s", options.game)
            exit(1)

        selected_set = sets_list[selected_game["name"]][int(options.set_id)]

        log.info("Scrap images of %s %s...", selected_game["clean_name"], selected_set["clean_name"])
        scrap_images(selected_game["clean_name"], selected_set["clean_name"], "en")
        #scrap_all(selected_game["name"], selected_set, csv_filename)

    if options.push:
        if options.game is None:
            log.error("Missing argument --game")
            exit(1)

        if options.set_id is None:
            log.error("Missing argument --set_id")
            exit(1)

        selected_game = None
        for game in games_list:
            if game["name"] == options.game:
                selected_game = game

        if selected_game is None:
            log.error("Unknown game %s", options.game)
            exit(1)

        selected_set = sets_list[selected_game["name"]][int(options.set_id)]

        if options.online and options.broadcast:
            log.error("Can't run with both online and broadcast flag.")
            exit(1)

        connection_list = []
        if options.online:
            connection_list.append("global")
        elif options.broadcast:
            connection_list.append("global")
            connection_list.append("local")
        else:
            connection_list.append("local")

        for connection_name in connection_list:
            log.info("Push set %s to db %s...", selected_set["clean_name"], connection_name)
            log.info("Load csv...")
            csv_filename = make_csv_filename(selected_game["name"], selected_set["code"])
            entries = load_csv(csv_filename)
            log.info("Push set...")
            set_lang_id = push_set_to_db(selected_game, selected_set, "en", options.commit, connection_name)
            log.info("Set added with id %d", set_lang_id)
            if options.clean_cards:
                log.info("Deleting cards from set %s...", set_lang_id)
                delete_cards_from_set_lang(set_lang_id, options.commit, connection_name)

            log.info("Push cards...")
            push_to_db(entries, selected_game, set_lang_id, options.commit, connection_name)

    if options.test_connection:
        connection_name = "local"
        if options.online is True:
            connection_name = "global"

        connection = get_connection(connection_name)
        sql = "select id from sets"
        cursor = connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) > 0:
            log.info("Connection success")
        else:
            log.error("Connection failed")

    log.info("Over")
