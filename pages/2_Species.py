import streamlit as st
from app_utils.session import initialize_session, update_species_selection
from app_utils.inaturalist import get_inaturalist_photo
from app_utils.maps import map_recordings
from streamlit_folium import st_folium


initialize_session()
recordings = st.session_state['recordings']
selected_recordings = st.session_state['selected_recordings']

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

m = map_recordings(selected_recordings)
st_folium(m, width=700, height=500)
