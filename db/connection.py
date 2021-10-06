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


def get_connection(connection_name):
    conn_info = mysql_connections[connection_name]
    connection = mysql.connector.connect(host=conn_info["host"], user=conn_info["user"], password=conn_info["password"], database=conn_info["db"])
    return connection
