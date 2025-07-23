import streamlit as st
from utils.db import check_user_credentials
from argon2 import PasswordHasher

ph = PasswordHasher()

def login_user():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_user_credentials(username, password):
            st.session_state.authenticated = True
            st.success("Logged in")
        else:
            st.error("Invalid username or password")
