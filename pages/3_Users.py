import streamlit as st
from utils.session import initialize_session

initialize_session()
data = st.session_state['data']

st.title("Users")
st.write("This is a page.")
