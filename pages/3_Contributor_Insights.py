import streamlit as st
from app_utils.session import initialize_session, render_sidebar
from app_utils import plots_contributor_insights

st.set_page_config(layout="wide")
render_sidebar()

initialize_session()
recordings = st.session_state['recordings']

st.title("Contributor Insights")

st.header("Highlights")

st.markdown(
    """This page describes the people who contribute the recordings."""
)

st.markdown(
    plots_contributor_insights.highlights(recordings)
)

st.header("Recordings per contributor trends")

st.plotly_chart(
    plots_contributor_insights.cumulative_contributors_by_recording_threshold(recordings)
)

st.plotly_chart(
    plots_contributor_insights.cumulative_recordings_versus_contributor_percentile(recordings)
)

st.header("Contributor retention trends")

st.plotly_chart(
    plots_contributor_insights.new_returning_by_month(recordings)
)

st.plotly_chart(
    plots_contributor_insights.contributor_retention(recordings)
)
