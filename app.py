import streamlit as st
import sqlite3
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

# DB Setup
def create_connection():
    conn = sqlite3.connect("users.db", check_same_thread=False)
    return conn

def create_users_table(conn):
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

conn = create_connection()
create_users_table(conn)

# Create a new user (signup)
def add_user(username, password):
    hashed_pwd = ph.hash(password)
    try:
        with conn:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pwd))
        return True
    except sqlite3.IntegrityError:
        return False

# Verify login credentials
def verify_user(username, password):
    user = conn.execute("SELECT password FROM users WHERE username = ?", (username,)).fetchone()
    if user:
        try:
            return ph.verify(user[0], password)
        except VerifyMismatchError:
            return False
    return False

# Login Page
def login_page():
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if verify_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"✅ Welcome, {username}!")
        else:
            st.error("❌ Invalid username or password.")

# Signup Page
def signup_page():
    st.subheader("📝 Signup")
    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")
    if st.button("Signup"):
        if add_user(new_user, new_pass):
            st.success("🎉 Account created! You can now log in.")
        else:
            st.error("🚫 Username already exists.")

# Main App
def main():
    st.title("🧠 Productivity App - Login System")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    menu = st.sidebar.selectbox("Menu", ["Login", "Signup"])

    if not st.session_state.logged_in:
        if menu == "Login":
            login_page()
        else:
            signup_page()
    else:
        st.success(f"🎉 Logged in as {st.session_state.username}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
        else:
            st.write("📋 Your dashboard goes here (to-do list, notes, etc.)")

if __name__ == "__main__":
    main()
