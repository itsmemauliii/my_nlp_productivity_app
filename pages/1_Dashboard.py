import streamlit as st
import sqlite3
from datetime import datetime

# Connect to SQLite DB (or create it if it doesn't exist)
conn = sqlite3.connect("data/productivity.db", check_same_thread=False)
cursor = conn.cursor()

# Create the productivity table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS productivity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    date TEXT,
    mood TEXT,
    tasks_done INTEGER,
    journal TEXT
)
""")
conn.commit()

st.set_page_config(page_title="Productivity Dashboard", page_icon="📈")
st.title("📈 Daily Productivity Tracker")

# Simulate logged-in user (you can pass from login logic in real app)
if 'username' not in st.session_state:
    st.warning("⚠️ Please login first!")
    st.stop()
username = st.session_state['username']

# Form to enter daily productivity
with st.form("productivity_form"):
    st.subheader("🗓️ Log Your Day")
    mood = st.selectbox("How was your mood today?", ["😀 Great", "🙂 Good", "😐 Okay", "😕 Bad", "😢 Terrible"])
    tasks_done = st.number_input("How many tasks did you complete today?", min_value=0, step=1)
    journal = st.text_area("Write a short journal (optional)")
    submitted = st.form_submit_button("💾 Save Entry")

    if submitted:
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO productivity (username, date, mood, tasks_done, journal) VALUES (?, ?, ?, ?, ?)",
                       (username, today, mood, tasks_done, journal))
        conn.commit()
        st.success("✅ Entry saved successfully!")

# Display past entries
st.subheader("📅 Your Past Logs")
cursor.execute("SELECT date, mood, tasks_done, journal FROM productivity WHERE username = ? ORDER BY date DESC", (username,))
data = cursor.fetchall()

if data:
    for row in data:
        st.markdown(f"**Date:** {row[0]}  ")
        st.markdown(f"**Mood:** {row[1]}  ")
        st.markdown(f"**Tasks Done:** {row[2]}  ")
        if row[3]:
            st.markdown(f"**Journal:** {row[3]}")
        st.markdown("---")
else:
    st.info("No logs yet. Start by entering your productivity for today!")
