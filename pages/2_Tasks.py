import streamlit as st
from utils.db import get_tasks, add_task, update_task_status
from utils.auth import login_user
from utils.nlp import analyze_text

st.set_page_config(page_title="Tasks", page_icon="✅", layout="centered")

st.markdown("<h1 style='text-align: center;'>✅ Your Daily Tasks</h1>", unsafe_allow_html=True)

if not st.session_state.get("logged_in"):
    st.warning("Please log in from the sidebar in Dashboard first.")
    st.stop()

st.markdown("### ➕ Add a New Task")

with st.form("task_form"):
    task_input = st.text_input("Enter a task")
    submit_task = st.form_submit_button("Add Task")
    if submit_task and task_input.strip() != "":
        add_task(st.session_state["username"], task_input)
        st.success("Task added!")

st.markdown("---")
st.markdown("### 📋 Your Task List")

tasks = get_tasks(st.session_state["username"])

if tasks:
    for task in tasks:
        task_id, task_text, is_done = task
        col1, col2 = st.columns([6, 1])
        with col1:
            st.write(f"- {'~~' + task_text + '~~' if is_done else task_text}")
            with st.expander("🔎 NLP Insights"):
                st.info(analyze_text(task_text))
        with col2:
            if st.checkbox("Done", value=is_done, key=f"task_{task_id}"):
                update_task_status(task_id, True)
            else:
                update_task_status(task_id, False)
else:
    st.info("No tasks added yet. Add one above.")
