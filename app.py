import streamlit as st
from utils.auth import check_login

st.set_page_config(page_title="NLP Productivity App", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Welcome to Your NLP Productivity Assistant")

if "logged_in" not in st.session_state:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_login(username, password):
            st.session_state.logged_in = True
            st.success("Welcome back, {}!".format(username))
        else:
            st.error("Invalid credentials")
else:
    st.success("You're logged in! Use the sidebar to explore.")
