import mysql.connector

mysql_connections = {}
mysql_connections["local"] = {}
mysql_connections["local"]["host"] = "localhost"
mysql_connections["local"]["user"] = "root"
mysql_connections["local"]["password"] = ""
mysql_connections["local"]["db"] = "wallstreet"

mysql_connections["global"] = {}
mysql_connections["global"]["host"] = "50.87.248.17"
mysql_connections["global"]["user"] = "vsquktmy_worker"
mysql_connections["global"]["password"] = "0aNb!Gs}2aIW"
mysql_connections["global"]["db"] = "vsquktmy_wallstreet"

conn_info = mysql_connections["local"]
connection = mysql.connector.connect(host=conn_info["host"], user=conn_info["user"], password=conn_info["password"], database=conn_info["db"])

sql = "select card.id as card_id, sets_langs.id as sets_langs_id from card inner join sets_langs on card.set_id = sets_langs.set_id where sets_langs.lang_id = 1"
cursor = connection.cursor()
cursor.execute(sql)
results = cursor.fetchall()

for card in results:
    sql = "update card set set_lang_id = %s where id = %s"
    values = [card[1], card[0]]
    cursor = connection.cursor()
    cursor.execute(sql, values)
    connection.commit()
