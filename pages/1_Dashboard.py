import streamlit as st
from utils.db import insert_journal_entry, get_today_summary
from utils.auth import login_user
from utils.nlp import analyze_text

st.set_page_config(page_title="Dashboard", page_icon="🧠", layout="centered")

st.markdown("<h1 style='text-align: center;'>🧠 Productivity Dashboard</h1>", unsafe_allow_html=True)

# Login Section
st.sidebar.header("🔐 Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
login_btn = st.sidebar.button("Login")

if login_btn:
    if login_user(username, password):
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.success(f"Welcome, {username}!")
    else:
        st.error("Invalid username or password.")

# If logged in
if st.session_state.get("logged_in"):
    st.markdown("### ✍️ Write your journal entry:")
    entry = st.text_area("How was your day?", height=150)

    if st.button("Save Entry"):
        if entry.strip() != "":
            insert_journal_entry(st.session_state["username"], entry)
            st.success("Your entry has been saved.")
        else:
            st.warning("Empty entry cannot be saved.")

    st.markdown("---")
    st.markdown("### 🪞 Daily Reflections")

    summaries = get_today_summary(st.session_state["username"])
    if summaries:
        for i, s in enumerate(summaries[::-1]):
            with st.expander(f"Entry {len(summaries) - i}"):
                st.write(s)
                st.markdown("##### 🧠 NLP Summary:")
                summary = analyze_text(s)
                st.info(summary)
    else:
        st.info("No entries yet for today. Write something above.")
else:
    st.warning("Please log in from the sidebar to access the dashboard.")

