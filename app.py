import streamlit as st
import pandas as pd
import hashlib
import os

# --- Utilities ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_user(username, password):
    df = pd.read_csv("users.csv")
    hashed_pw = hash_password(password)
    return not df[(df["username"] == username) & (df["password"] == hashed_pw)].empty

def create_user(username, password):
    df = pd.read_csv("users.csv")
    if username in df["username"].values:
        return False  # User already exists
    new_user = pd.DataFrame({"username": [username], "password": [hash_password(password)]})
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv("users.csv", index=False)
    return True

# --- Login Page ---
def login_page():
    st.title("🔐 Login to Productivity App")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if check_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("✅ Login successful!")
            st.experimental_rerun()
        else:
            st.error("❌ Invalid credentials")

    if st.button("Go to Signup"):
        st.session_state.page = "signup"
        st.experimental_rerun()

# --- Signup Page ---
def signup_page():
    st.title("📝 Create an Account")
    username = st.text_input("Choose a username")
    password = st.text_input("Choose a password", type="password")

    if st.button("Signup"):
        if create_user(username, password):
            st.success("🎉 Account created! You can now log in.")
            st.session_state.page = "login"
            st.experimental_rerun()
        else:
            st.error("⚠️ Username already taken!")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.experimental_rerun()

# --- Main App after Login ---
def main_app():
    st.title("🚀 Welcome to the NLP Productivity App")
    st.write(f"👋 Hello **{st.session_state.username}**!")
    st.markdown("Start building your productivity workflow here...")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()

# --- Routing ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "login"

if st.session_state.logged_in:
    main_app()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
