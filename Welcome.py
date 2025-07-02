import streamlit as st
from app_utils.session import initialize_session, render_sidebar, load_recordings
from app_utils.inaturalist import get_inaturalist_photo

st.set_page_config(layout="wide")
initialize_session()
render_sidebar()

st.title("Welcome to the warbler dashboard")

left, right = st.columns(2)

with left:
    first_month = st.session_state.get('first_month')
    last_month = st.session_state.get('last_month')
    f"""
    This dashboard summarizes audio recordings of warblers in the United States 
    that have been contributed to [Xeno-canto](https://xeno-canto.org), a global repository of nature sound 
    recordings shared under Creative Commons licenses. It demonstrates how web service 
    usage can be analyzed over time, across contributors, and by content type. 
    The data include recordings uploaded from {first_month} to {last_month}.
    
    Warblers are small, often colorful songbirds known for their energetic behavior 
    and distinctive vocalizations. Their songs are typically high-pitched, rapid, 
    and complex—often used for communication and attracting mates during the breeding 
    season. Warblers are a favorite among birders and bioacoustics researchers due to 
    the variety and intricacy of their calls.
    
    The sidebar provides navigation to the pages of the dashboard, which include:
    
      - **Recording Trends**: An overview of recording activity by location, over time, and by species
      - **Recording Quality**: A summary of quality ratings, including how they vary by time and recording device
      - **Contributor Insights**: An analysis of contributor behavior, including activity patterns and retention
      - **Species Insights** Tools to filter recordings by species, compare trends across species, and access example recordings
      
    This project relies on data retrieved from [xeno-canto.org](https://xeno-canto.org/)
    and photographs from [inaturalist.org](https://www.inaturalist.org/),
    all of which are made available under Creative Commons licenses. Individual creators
    are credited within the dashboard wherever their works are referenced. 
    The project itself is licensed under
    [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0).
    """

with right:
    recordings = load_recordings()
    birds = recordings[['en', 'scientific_name']].drop_duplicates().sample(frac=1)

    n_photos = 2
    photos = []
    for _, row in birds.iterrows():
        url, credit = get_inaturalist_photo(row['scientific_name'])
        if url is not None:
            photos.append({'en': row['en'], 'url': url, 'credit': credit})
        if len(photos) == n_photos:
            break

    for photo in photos:
        st.image(photo['url'])
        st.markdown(photo['en'] + '. ' + photo['credit'])
