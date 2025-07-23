import streamlit as st
from auth import login
from db import init_db, save_entry, get_all_entries
from nlp_analysis import analyze_text
import pandas as pd

# Page setup
st.set_page_config(page_title="NLP Productivity App", layout="wide")

# DB init
init_db()

# User login
if not login():
    st.stop()

# Session state
if "entries" not in st.session_state:
    st.session_state.entries = get_all_entries()

# UI
st.title("📔 NLP Productivity Tracker")

with st.form("task_form"):
    st.subheader("📝 Add Your Task or Journal Entry")
    content = st.text_area("Write here...", height=150)
    submitted = st.form_submit_button("Analyze & Save")
    if submitted and content:
        sentiment, keywords = analyze_text(content)
        save_entry(content, sentiment, ", ".join(keywords))
        st.success("Saved and analyzed.")
        st.session_state.entries = get_all_entries()

# Display Entries
if st.session_state.entries:
    df = pd.DataFrame(st.session_state.entries, columns=["Text", "Sentiment", "Keywords", "Timestamp"])
    st.dataframe(df)

    st.subheader("📊 Sentiment Summary")
    st.bar_chart(df["Sentiment"].value_counts())

