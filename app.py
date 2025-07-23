# app.py
import streamlit as st
import sqlite3
from argon2 import PasswordHasher
import os

ph = PasswordHasher()

# DB setup
def init_db():
    conn = sqlite3.connect("productivity.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 username TEXT PRIMARY KEY,
                 password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Signup page
def signup_page():
    st.title("Sign Up")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        conn = sqlite3.connect("productivity.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (new_user,))
        if c.fetchone():
            st.error("Username already exists")
        else:
            hashed_pwd = ph.hash(new_password)
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_user, hashed_pwd))
            conn.commit()
            st.success("User registered! Please log in.")
        conn.close()

# Login page
def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        conn = sqlite3.connect("productivity.db")
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?", (username,))
        data = c.fetchone()
        conn.close()
        if data:
            try:
                ph.verify(data[0], password)
                st.session_state['username'] = username
                st.success("Login successful!")
                st.switch_page("1_Dashboard.py")
            except:
                st.error("Incorrect password")
        else:
            st.error("User not found")

# Main
st.set_page_config(page_title="NLP Productivity App", layout="centered")
if 'username' not in st.session_state:
    menu = ["Login", "Sign Up"]
    choice = st.selectbox("Menu", menu)
    if choice == "Login":
        login_page()
    else:
        signup_page()
else:
    st.switch_page("1_Dashboard.py")
