import streamlit as st
from utils.session import initialize_session
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium


initialize_session()
data = st.session_state['data']

st.title("Overview")
st.write("This is a page.")

heat_data = [(row['lat'], row['lon']) for _, row in data.iterrows()]
m = folium.Map(location=[39, -97], zoom_start=4)
HeatMap(heat_data, radius=20).add_to(m)
st_folium(m, width=700, height=500)