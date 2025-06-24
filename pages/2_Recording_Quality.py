import streamlit as st
from app_utils.session import initialize_session
from app_utils import plots_recording_quality

st.set_page_config(layout="wide")

initialize_session()
recordings = st.session_state['recordings']

st.title("Recording Quality")

st.header('Distribution of ratings')

st.plotly_chart(
    plots_recording_quality.recordings_by_quality(recordings)
)

st.header('Temporal trends for ratings')

st.plotly_chart(
    plots_recording_quality.quality_by_year(recordings)
)

st.header('Device trends for ratings')

st.plotly_chart(
    plots_recording_quality.quality_verus_popularity(recordings)
)

left, right = st.columns(2)
with left:
    st.plotly_chart(
        plots_recording_quality.top_devices_popularity(recordings)
        .update_layout(height=300)
    )
with right:
    st.plotly_chart(
        plots_recording_quality.top_devices_quality(recordings)
        .update_layout(height=300)
    )

