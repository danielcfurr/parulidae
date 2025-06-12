import streamlit as st
from utils.session import initialize_session, update_species_selection
from utils.inaturalist import get_inaturalist_photo

initialize_session()
data = st.session_state['data']

st.title("Species")
st.write("This is a page.")

st.selectbox(
    "Species",
    options=st.session_state['common_names'],
    index=st.session_state['selected_index'],
    key='selected_common',
    on_change=update_species_selection
)

get_inaturalist_photo(st.session_state['selected_scientific'])

import folium
from streamlit_folium import st_folium

# Create the folium map
m = folium.Map(
    location=[39, -97],
    zoom_start=4,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr='Esri',
)

points = [{'lat': row['lat'], 'lon': row['lon'], 'name': idx} for idx, row in st.session_state['selected_data'].iterrows()]

for pt in points:
    folium.Marker(
        location=[pt['lat'], pt['lon']],
        tooltip=pt['name'],
        popup=pt['name']
    ).add_to(m)

st_folium(m, width=700, height=500)
