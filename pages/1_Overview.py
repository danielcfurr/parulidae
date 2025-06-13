import streamlit as st
from app_utils.session import initialize_session
from app_utils.maps import map_heat
from streamlit_folium import st_folium


initialize_session()
recordings = st.session_state['recordings']

st.title("Overview")
st.write("This is a page.")

m = map_heat(recordings)
st_folium(m, width=700, height=500)
