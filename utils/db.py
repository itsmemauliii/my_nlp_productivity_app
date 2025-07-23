import sqlite3
from datetime import datetime

def create_connection():
    return sqlite3.connect("data/productivity.db", check_same_thread=False)

def insert_journal_entry(username, journal_text, mood):
    conn = create_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO journal (username, journal_text, mood, timestamp) VALUES (?, ?, ?, ?)",
        (username, journal_text, mood, datetime.now()),
    )
    conn.commit()
    conn.close()

def get_today_summary(username):
    conn = create_connection()
    c = conn.cursor()
    c.execute(
        "SELECT journal_text, mood, timestamp FROM journal WHERE username = ? ORDER BY timestamp DESC LIMIT 5",
        (username,),
    )
    rows = c.fetchall()
    conn.close()
    return rows
