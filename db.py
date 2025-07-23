import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("data/entries.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            content TEXT,
            sentiment TEXT,
            keywords TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_entry(content, sentiment, keywords):
    conn = sqlite3.connect("data/entries.db")
    c = conn.cursor()
    c.execute("INSERT INTO entries VALUES (?, ?, ?, ?)", (content, sentiment, keywords, datetime.now()))
    conn.commit()
    conn.close()

def get_all_entries():
    conn = sqlite3.connect("data/entries.db")
    c = conn.cursor()
    c.execute("SELECT * FROM entries ORDER BY timestamp DESC")
    entries = c.fetchall()
    conn.close()
    return entries
