import streamlit as st
from utils.auth import login_user
from utils.db import init_db

st.set_page_config(page_title="NLP Productivity App", layout="wide")

# Initialize database
init_db()

# Simple routing for login and main app
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    login_user()
else:
    st.sidebar.success("Logged in successfully")
    st.switch_page("pages/1_Dashboard.py")
