import sqlite3
from datetime import datetime

DB_PATH = "data/productivity.db"

def create_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

def initialize_database():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS journal_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        date TEXT NOT NULL,
        entry TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        task TEXT NOT NULL,
        completed BOOLEAN DEFAULT 0,
        date_created TEXT,
        date_completed TEXT
    )
    """)

    conn.commit()
    conn.close()

def check_user_credentials(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    record = cursor.fetchone()
    conn.close()
    if record:
        return record[0]
    return None

def insert_journal_entry(username, entry):
    conn = create_connection()
    cursor = conn.cursor()
    today = datetime.today().strftime('%Y-%m-%d')
    cursor.execute("""
        INSERT INTO journal_entries (username, date, entry)
        VALUES (?, ?, ?)
    """, (username, today, entry))
    conn.commit()
    conn.close()

def get_today_summary(username):
    conn = create_connection()
    cursor = conn.cursor()
    today = datetime.today().strftime('%Y-%m-%d')
    cursor.execute("""
        SELECT entry FROM journal_entries
        WHERE username = ? AND date = ?
    """, (username, today))
    records = cursor.fetchall()
    conn.close()
    return [r[0] for r in records]

def insert_task(username, task):
    conn = create_connection()
    cursor = conn.cursor()
    date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
        INSERT INTO tasks (username, task, date_created)
        VALUES (?, ?, ?)
    """, (username, task, date_created))
    conn.commit()
    conn.close()

def get_tasks(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, task, completed FROM tasks
        WHERE username = ?
    """, (username,))
    records = cursor.fetchall()
    conn.close()
    return records

def complete_task(task_id):
    conn = create_connection()
    cursor = conn.cursor()
    date_completed = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
        UPDATE tasks SET completed = 1, date_completed = ?
        WHERE id = ?
    """, (date_completed, task_id))
    conn.commit()
    conn.close()

def get_task_stats(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT completed, COUNT(*) FROM tasks
        WHERE username = ?
        GROUP BY completed
    """, (username,))
    stats = cursor.fetchall()
    conn.close()
    return stats
