import streamlit as st
from app_utils.session import initialize_session, update_species_selection, render_sidebar
from app_utils.inaturalist import get_inaturalist_photo
from app_utils.maps import map_recordings
from app_utils import plots_species_insights
from streamlit_folium import folium_static

st.set_page_config(layout="wide")
initialize_session()
render_sidebar()

recordings = st.session_state['recordings']

st.title("Species insights")

"""
This page provides tools to filter recordings by species, compare 
trends across species, and access example recordings. Please select
a species to explore.
"""

species = st.selectbox(
    "Selected species:",
    options=st.session_state['common_names'],
    index=st.session_state['selected_index'],
)

update_species_selection(species)

st.header(f'Highlights for {species}')

photo_url, photo_text = get_inaturalist_photo(st.session_state['selected_scientific'])
left, right = st.columns(2)
with left:
    st.markdown(plots_species_insights.highlights(recordings, species))
    st.markdown(photo_text)
with right:
    if photo_url is not None:
        st.image(photo_url)

st.header(f'Recording locations for {species}')

"""Click on map pins to access information about the recordings, including a link to hear them."""

folium_static(
    map_recordings(recordings, species),
    width=700,
    height=500
)

st.header(f'Temporal trends for {species}')

left, right = st.columns(2)
with left:
    st.plotly_chart(
        plots_species_insights.recordings_by_month(recordings, species)
    )
with right:
    st.plotly_chart(
        plots_species_insights.recordings_by_year(recordings, species)
    )

st.header(f'{species} compared to other species')

left, right = st.columns(2)
with left:
    st.plotly_chart(
        plots_species_insights.recordings_versus_other_species(recordings, species)
    )
with right:
    st.plotly_chart(
        plots_species_insights.ratings_versus_other_species(recordings, species)
    )
