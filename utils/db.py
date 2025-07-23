import sqlite3
from argon2 import PasswordHasher

ph = PasswordHasher()

def init_db():
    conn = sqlite3.connect("data/productivity.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    # Optional: Add a sample user for testing
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       ("testuser", ph.hash("testpass")))
    except sqlite3.IntegrityError:
        pass
    conn.commit()
    conn.close()

def check_user_credentials(username, password):
    conn = sqlite3.connect("data/productivity.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    record = cursor.fetchone()
    conn.close()
    if record:
        try:
            return ph.verify(record[0], password)
        except:
            return False
    return False
