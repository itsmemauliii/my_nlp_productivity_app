import streamlit as st
import hashlib
from utils.db import check_user_credentials

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.subheader("🔐 Login to Your Productivity Hub")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            hashed_pw = hash_password(password)
            if check_user_credentials(username, hashed_pw):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Welcome back, {} 👋".format(username))
                st.experimental_rerun()
            else:
                st.error("Invalid username or password.")
    return st.session_state.logged_in
