import streamlit as st
from app_utils.session import initialize_session

initialize_session()
recordings = st.session_state['recordings']

st.title("Users")
st.write("This is a page.")
