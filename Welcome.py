import streamlit as st
from app_utils.session import initialize_session, render_sidebar

st.set_page_config()
render_sidebar()

initialize_session()

st.title("Welcome")
st.write("This is the first page shown when the app starts.")
