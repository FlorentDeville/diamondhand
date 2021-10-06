import argparse

import json
import logging
import lxml.html
import mysql.connector
import os
import re
import sys
import time

from argparse import RawTextHelpFormatter
from selenium import webdriver

sys.path.append("../")
from db.connection import get_connection
from db.db_pokemon import DbPokemon
from db.db_fftcg import DbFFTcg

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
    browser = webdriver.Chrome(executable_path="C:/workspace/python/chromedriver.exe", chrome_options=chromeOptions)

    filename = csv_filename
    if game_name == "pokemon":
        db = DbPokemon(browser, filename)
    elif game_name == "fftcg":
        db = DbFFTcg(browser, filename)

    search_url_pattern = set["url"]

    page_count = set["page_count"]
    for page_id in range(1, page_count + 1):
        log.info("Scrap page %d of %d...", page_id, page_count)
        complete_search_url = search_url_pattern.format(page_id)

        browser.get(complete_search_url)
        time.sleep(2)
        text_html = browser.execute_script("return document.body.innerHTML")
        html = lxml.html.fromstring(text_html)

        xpath_cards = "//div[contains(@class, 'search-result__content')]/a"
        elements = html.xpath(xpath_cards)

        for element in elements:
            card_url = element.attrib.get('href')
            card_url = "http://tcgplayer.com" + card_url

            log.info(card_url + "...")
            entry = db.scrap_card_information(card_url, set["code"])

            log.info("writing to csv...")
            db.write(entry)

    browser.close()


def load_csv(csv_filename):
    db = DbFFTcg(None, csv_filename)
    entries = db.load()
    return entries


# Push a set to the db and return its id
def push_set_to_db(selected_game, selected_set, commit, connection_name):
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
    if len(results) > 0:
        return results[0][0]  # the set already exists in the db

    # add the set
    sql = "insert into sets (name, code, release_date, game_id) values (%s, %s, %s, %s)"
    sql_values = [selected_set["clean_name"], selected_set["code"], selected_set["release_date"], game_id]
    cursor = connection.cursor()
    cursor.execute(sql, sql_values)
    if commit:
        connection.commit()

    return cursor.lastrowid


# Push all entries to the cards table
def push_to_db(entries, selected_game, set_id, variation, commit, connection_name):
    connection = get_connection(connection_name)

    for card in entries:
        cardInsertSql = "insert into card (name, set_id, rarity, variation, tcg_url, number) values (%s, %s, %s, %s, %s, %s)"

        # extract the card number from the fftcg number which is <opus>-<number><rarity>
        if selected_game["name"] == "fftcg":
            pattern = "\\d*-(\\d*)."
            matches = re.match(pattern, card.number)
            number = matches.group(1)
        else:
            number = card.number

        cardInsertSqlValues = [card.name, set_id, card.rarity, variation, card.tcg_url, int(number)]
        cursor = connection.cursor()

        # If the commit flag is false then we didn't push the set so the set_id doesn't exist.
        # Executing the request will trigger a foreign key execption.
        if commit:
            cursor.execute(cardInsertSql, cardInsertSqlValues)
            connection.commit()


def make_csv_filename(game_name, set_name):
    csv_filename = "C:\\workspace\\python\\data\\%s\\db_%s.csv" % (game_name, set_name)
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

    parser = argparse.ArgumentParser(description="Parse tcgplayer to create the list of cards in a set of FFTCG.", formatter_class=RawTextHelpFormatter)

    game_help_text = "Index of games:\n"
    for game in games_list:
        game_help_text += "\t%s\n" % (game["name"])

    parser.add_argument('--game', '-g', dest="game", help=game_help_text)
    parser.add_argument('--list-sets', dest="list_sets", action="store_true", default=False, help="List the sets for the selected game")
    parser.add_argument('--set-id', '-s', dest="set_id", help="Index of the set to work with")
    parser.add_argument("--scrap", dest="scrap", action="store_true", default=False, help="Scrap the data from tcgplayer.")
    parser.add_argument("--push", "-p", dest="push", action="store_true", default=False, help="Push csv file to database.")
    parser.add_argument('--commit', '-c', dest="commit", action="store_true", default=False, help="Commit to the database.")
    parser.add_argument('--online', '-o', dest="online", action="store_true", default=False, help="Push to the online db. By default, push to the local db.")
    parser.add_argument('--test-connection', '-t', dest="test_connection", action="store_true", default=False, help="Test the mysql connection.")
    options = parser.parse_args()
    log.info("Start...")

    if options.list_sets:
        if options.game is None:
            log.error("Missing -g argument")
            exit(1)

        sets = sets_list[options.game]
        for index in range(len(sets)):
            log.info("%d : %s", index, sets[index]["clean_name"])

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
        csv_filename = make_csv_filename(selected_game["name"], selected_set["name"])
        scrap_all(selected_game["name"], selected_set, csv_filename)

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

        connection_name = "local"
        if options.online is True:
            connection_name = "global"

        log.info("Push set %s to db %s...", selected_set["clean_name"], connection_name)
        log.info("Load csv...")
        csv_filename = make_csv_filename(selected_game["name"], selected_set["name"])
        entries = load_csv(csv_filename)
        log.info("Push set...")
        set_id = push_set_to_db(selected_game, selected_set, options.commit, connection_name)
        log.info("Set added with id %d", set_id)
        log.info("Push cards...")
        push_to_db(entries, selected_game, set_id, None, options.commit, connection_name)

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
