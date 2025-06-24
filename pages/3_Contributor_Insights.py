import streamlit as st
from app_utils.session import initialize_session
from app_utils import plots_contributor_insights

st.set_page_config(layout="wide")

initialize_session()
recordings = st.session_state['recordings']

st.title("Contributor Insights")

st.plotly_chart(
    plots_contributor_insights.cumulative_contributors_by_recording_threshold(recordings)
)

st.plotly_chart(
    plots_contributor_insights.cumulative_recordings_versus_contributor_percentile(recordings)
)

st.plotly_chart(
    plots_contributor_insights.new_returning_by_month(recordings)
)

st.plotly_chart(
    plots_contributor_insights.contributor_retention(recordings)
)
