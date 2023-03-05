import logging
import lxml.html
import os
import urllib
import sys
import time

sys.path.append("../")

from db.connection import get_connection
from selenium import webdriver

log = logging.getLogger(__name__)


def find_set_lang_id(game_name, set_name, lang_code):
    connection = get_connection("local")

    sql = "select id from game where game.name=%s"
    sql_values = [game_name]
    cursor = connection.cursor()
    cursor.execute(sql, sql_values)
    results = cursor.fetchall()
    if len(results) != 1:
        log.info("Can't find game id for %s", game_name)
        return -1

    game_id = results[0][0]

    #check if the set is already there
    sql = "select id from sets where sets.name=%s and sets.game_id=%s"
    sql_values = [set_name, game_id]
    cursor = connection.cursor()
    cursor.execute(sql, sql_values)
    results = cursor.fetchall()
    set_id = -1
    if len(results) != 1:
        log.info("Can't find set id for game id %d and set name %s", game_id, set_name)
        return -1
    
    set_id = results[0][0]  # the set already exists in the db

    # get the lang id
    sql = "select id from languages where code = %s"
    sql_values=[lang_code]
    cursor = connection.cursor()
    cursor.execute(sql, sql_values)
    results = cursor.fetchall()
    lang_id = -1
    if len(results) != 1:
        log.exception("Unknown language %s", lang_code)
        return -1

    lang_id = results[0][0]

    # check if the set_lang is there
    sql = "select id from sets_langs where set_id = %s and lang_id = %s"
    sql_values = [set_id, lang_id]
    cursor = connection.cursor()
    cursor.execute(sql, sql_values)
    results = cursor.fetchall()
    set_lang_id = -1
    if len(results) != 1:
        log.exception("Can't find set_lang setId=%s, langId=%d", set_id, lang_id)
        return-1

    set_lang_id = results[0][0]
    return set_lang_id


def scrap_images(game_name, set_name, lang_code):
    connection = get_connection("local")

    set_lang_id = find_set_lang_id(game_name, set_name, lang_code)
    if set_lang_id == -1:
        return None

    #save image to folder
    dstFolder = ".\\..\\ui\\pics\\sets\\" + str(set_lang_id)
    log.info("Creating folder %s", dstFolder)
    if not os.path.exists(dstFolder):
        os.mkdir(dstFolder)

    log.info("Setup webdriver...")
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--start-maximized")
    browser = webdriver.Chrome(executable_path="C:/workspace/DiamondHand/chromedriver.exe", chrome_options=chromeOptions)

    log.info("Found set_lang_id %d", set_lang_id)

    sql = "select id, tcg_url from card where set_lang_id=%s"
    sql_values = [set_lang_id]
    cursor = connection.cursor()
    cursor.execute(sql, sql_values)
    results = cursor.fetchall()

    cardCount = len(results)
    log.info("Found %d cards", cardCount)
    for ii in range(cardCount):
        card = results[ii]

        cardUrl = card[1]
        browser.get(cardUrl)
        TIME_TO_WAIT = 4
        time.sleep(TIME_TO_WAIT)
        text_html = browser.execute_script("return document.body.innerHTML")
        html = lxml.html.fromstring(text_html)

        search_xpath = "//div[contains(@class, 'lazy-image__wrapper')]/img"
        elements = html.xpath(search_xpath)
        elementsCount = len(elements)
        if elementsCount == 0:
            log.info("Failed to find url for %s", cardUrl)
            continue

        image_url = elements[0].attrib.get("src")
        log.info("[%d/%d] %s", ii + 1, cardCount, image_url)

        dstFile = dstFolder + "\\" + str(card[0]) + ".png"
        urllib.urlretrieve(image_url, dstFile) 

        log.info("    File saved %s", dstFile)
        


    browser.close()


