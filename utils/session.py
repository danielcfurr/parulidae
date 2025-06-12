import streamlit as st
from .data import load_clean_data


def initialize_session() -> None:
    initialized = st.session_state.get("initialized", False)
    if not initialized:
        st.session_state['initialized'] = True

        data = load_clean_data()
        st.session_state['data'] = data

        names = data[['en', 'scientific_name']].drop_duplicates().sort_values(['en', 'scientific_name'])
        st.session_state['common_names'] = names['en']
        st.session_state['scientific_names'] = names['scientific_name']
        st.session_state['selected_common'] = st.session_state['common_names'].iloc[0]

        update_species_selection()


def update_species_selection():
    common_name = st.session_state['selected_common']
    idx = list(st.session_state['common_names']).index(common_name)
    st.session_state['selected_index'] = idx
    st.session_state['selected_scientific'] = st.session_state['scientific_names'].iloc[idx]
    data = st.session_state['data']
    st.session_state['selected_data'] = data.loc[data['en'] == common_name]

