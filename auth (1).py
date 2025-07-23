import streamlit as st

def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        with st.form("login_form"):
            st.subheader("🔐 Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")

            if login_button:
                if username == "admin" and password == "password123":
                    st.session_state.logged_in = True
                    st.success("Welcome!")
                else:
                    st.error("Invalid credentials")

    return st.session_state.logged_in
