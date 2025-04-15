import sqlite3
from sqlite3 import Error


class User:

    def __init__(self, database):
        self.database = database
        conn = sqlite3.connect('test.db')
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection