import streamlit as st
from utils.db import get_journal_entries, get_tasks
from wordcloud import WordCloud
from utils.auth import login_user
from collections import Counter
import matplotlib.pyplot as plt
from utils.nlp import analyze_text, get_sentiment_score

st.set_page_config(page_title="Stats", page_icon="📈", layout="wide")

st.markdown("<h1 style='text-align: center;'>📈 Productivity Stats</h1>", unsafe_allow_html=True)

if not st.session_state.get("logged_in"):
    st.warning("Please log in from the sidebar in Dashboard first.")
    st.stop()

username = st.session_state["username"]

# ========== TASK ANALYSIS ==========
st.subheader("✅ Task Completion Overview")
tasks = get_tasks(username)

if tasks:
    total = len(tasks)
    completed = sum(1 for t in tasks if t[2])
    pending = total - completed

    labels = ["Completed", "Pending"]
    sizes = [completed, pending]
    colors = ["#36d6ae", "#ff6b6b"]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    ax1.axis("equal")
    st.pyplot(fig1)
else:
    st.info("No tasks to analyze.")

# ========== JOURNAL NLP ANALYSIS ==========
st.subheader("📝 Journal Sentiment & WordCloud")

entries = get_journal_entries(username)

if entries:
    texts = [entry[1] for entry in entries]
    full_text = " ".join(texts)

    # Sentiment breakdown
    sentiment_scores = [get_sentiment_score(t) for t in texts]
    avg_sentiment = round(sum(sentiment_scores) / len(sentiment_scores), 2)

    st.metric("Average Sentiment Score", avg_sentiment)

    # Word Cloud
    word_freq = Counter(" ".join(full_text.lower().split()).split())

    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_freq)
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.imshow(wordcloud, interpolation="bilinear")
    ax2.axis("off")
    st.pyplot(fig2)
else:
    st.info("No journal entries found.")
