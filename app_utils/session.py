import streamlit as st
import pandas as pd
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = THIS_DIR.parent
CLEAN_DATA_DIR = PROJECT_DIR / "data" / "clean"


def initialize_session() -> None:
    initialized = st.session_state.get("initialized", False)
    if not initialized:
        st.session_state['initialized'] = True

        recordings = load_recordings()
        st.session_state['recordings'] = recordings
        st.session_state['monthly'] = load_monthly()

        month = recordings['uploaded'].dt.to_period("M").dt.to_timestamp()
        st.session_state['first_month'] = month.min().strftime('%B %Y')
        st.session_state['last_month'] = month.max().strftime('%B %Y')

        names = recordings[['en', 'scientific_name']].drop_duplicates().sort_values(['en', 'scientific_name'])
        st.session_state['common_names'] = names['en']
        st.session_state['scientific_names'] = names['scientific_name']

        # Set default values for species selection
        common_name = st.session_state['common_names'].iloc[0]
        update_species_selection(common_name)


def update_species_selection(common_name: str):
    st.session_state['selected_common'] = common_name
    idx = list(st.session_state['common_names']).index(common_name)
    st.session_state['selected_index'] = idx
    st.session_state['selected_scientific'] = st.session_state['scientific_names'].iloc[idx]


def load_recordings():
    recordings = pd.read_csv(CLEAN_DATA_DIR / "recordings.csv", index_col='id')

    # Combine scientific name
    recordings['scientific_name'] = recordings['gen'] + ' ' + recordings['sp']

    # Fix up dates
    recordings['date'] = pd.to_datetime(recordings['date'])
    recordings['uploaded'] = pd.to_datetime(recordings['uploaded'])

    # Create numerical values to quality ratings
    recordings['q_num'] = recordings['q'].map({'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0})
    recordings.loc[recordings['q_num'].isna(), 'q'] = pd.NA

    # Remove most recent month because it is incomplete
    latest_month = recordings['uploaded'].dt.to_period("M").dt.to_timestamp().max()
    recordings = recordings.loc[recordings['uploaded'] < latest_month]

    return recordings


def load_monthly():
    monthly = pd.read_csv(CLEAN_DATA_DIR / "monthly.csv")
    monthly['month'] = pd.to_datetime(monthly['month'])
    monthly.set_index('month')
    return monthly


def render_sidebar():
    first_month = st.session_state.get('first_month')
    last_month = st.session_state.get('last_month')

    st.sidebar.markdown(
        f"""
        This dashboard summarizes [xeno-canto](https://xeno-canto.org/) recordings of 
        US warblers from {first_month} to {last_month}.
        """
    )