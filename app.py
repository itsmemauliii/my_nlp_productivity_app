import streamlit as st
from utils.auth import check_login
from textblob import download_corpora
download_corpora.download_all()

st.set_page_config(page_title="NLP Productivity App", layout="wide")

# Session state login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

st.title("🔐 Welcome to Your NLP Productivity Tracker")

if not st.session_state.logged_in:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if check_login(username, password):
            st.success("✅ Logged in successfully!")
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("🚫 Invalid credentials. Please try again.")
else:
    st.sidebar.success("✅ You are logged in.")
    st.sidebar.page_link("pages/1_Dashboard.py", label="📔 Dashboard")
    st.sidebar.page_link("pages/2_Tasks.py", label="🧠 Tasks")
    st.sidebar.page_link("pages/3_Analytics.py", label="📊 Analytics")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))
