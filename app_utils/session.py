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

        names = recordings[['en', 'scientific_name']].drop_duplicates().sort_values(['en', 'scientific_name'])
        st.session_state['common_names'] = names['en']
        st.session_state['scientific_names'] = names['scientific_name']
        st.session_state['selected_common'] = st.session_state['common_names'].iloc[0]

        update_species_selection()


def update_species_selection():
    common_name = st.session_state['selected_common']
    idx = list(st.session_state['common_names']).index(common_name)
    st.session_state['selected_index'] = idx
    st.session_state['selected_scientific'] = st.session_state['scientific_names'].iloc[idx]
    recordings = st.session_state['recordings']
    st.session_state['selected_recordings'] = recordings.loc[recordings['en'] == common_name]


def load_recordings():
    recordings = pd.read_csv(CLEAN_DATA_DIR / "recordings.csv", index_col='id')
    recordings['scientific_name'] = recordings['gen'] + ' ' + recordings['sp']
    recordings['date'] = pd.to_datetime(recordings['date'])
    recordings['uploaded'] = pd.to_datetime(recordings['uploaded'])
    recordings['q'] = recordings['q'].astype(pd.CategoricalDtype(categories=['A', 'B', 'C', 'D', 'E'], ordered=True))
    return recordings


def load_monthly():
    monthly = pd.read_csv(CLEAN_DATA_DIR / "monthly.csv")
    monthly['month'] = pd.to_datetime(monthly['month'])
    monthly.set_index('month')
    return monthly

