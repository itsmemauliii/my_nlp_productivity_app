import streamlit as st
import sqlite3
from utils.db import create_connection, insert_journal_entry, get_today_summary
from utils.auth import check_login
from datetime import datetime
from textblob import TextBlob

st.set_page_config(page_title="Productivity Dashboard", layout="wide")

# -------------- LOGIN CHECK --------------
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("You must log in first.")
    st.stop()

# -------------- PAGE TITLE --------------
st.title("📊 Productivity Dashboard")

# -------------- DATABASE --------------
conn = create_connection()

# -------------- JOURNAL SECTION --------------
st.subheader("📝 Daily Journal")
with st.form("journal_form"):
    journal_text = st.text_area("How did your day go?", height=150)
    submitted = st.form_submit_button("Analyze & Save")

    if submitted and journal_text.strip() != "":
        # NLP SENTIMENT ANALYSIS
        blob = TextBlob(journal_text)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            sentiment = "😊 Positive"
        elif polarity < -0.1:
            sentiment = "☹️ Negative"
        else:
            sentiment = "😐 Neutral"

        # Save to DB
        insert_journal_entry(conn, st.session_state['username'], journal_text, sentiment)

        st.success(f"Sentiment: {sentiment}")

# -------------- TODAY'S SUMMARY --------------
st.subheader("📌 Today's Mood Summary")
summary = get_today_summary(conn, st.session_state['username'])
if summary:
    st.write(f"🗓️ Date: {summary['date']}")
    st.write(f"✍️ Journal: {summary['entry']}")
    st.write(f"📈 Sentiment: {summary['sentiment']}")
else:
    st.info("No journal entry found for today.")
