import streamlit as st
from app_utils.session import initialize_session, render_sidebar
from app_utils.maps import map_heat
from app_utils import plots_recording_trends
from streamlit_folium import folium_static

st.set_page_config(layout="wide")
render_sidebar()

initialize_session()
recordings = st.session_state['recordings']
monthly = st.session_state['monthly']

st.title("Recording Trends")

st.header("Highlights")

st.markdown(
    """This page provides an overview of warbler recording uploads."""
)

st.markdown(
    plots_recording_trends.highlights(recordings)
)

st.header("Geographic trends")

st.markdown('**Heat map for recording locations**')
folium_static(
    map_heat(recordings),
    width=700,
    height=500,
)

st.header("Temporal trends")

st.plotly_chart(
    plots_recording_trends.uploads_by_month_year(monthly)
)

left, right = st.columns(2)
with left:
    st.plotly_chart(
        plots_recording_trends.uploads_by_month(monthly)
    )
with right:
    st.plotly_chart(
        plots_recording_trends.uploads_by_year(recordings)
    )

st.header("Species trends")

st.plotly_chart(
    plots_recording_trends.uploads_by_species(recordings).update_layout(height=1000),
)
