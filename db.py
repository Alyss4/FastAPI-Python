import sqlite3

DB_FILE = "demo.db"

def getconnection():
    return sqlite3.connect(DB_FILE)