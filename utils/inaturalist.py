import requests
import streamlit as st


def get_inaturalist_photo(scientific_name):
    base_url = "https://api.inaturalist.org/v1/taxa"
    params = {"q": scientific_name}

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print(f"Request failed with status {response.status_code}")
        return

    data = response.json()
    results = data.get("results")
    if not results:
        print("No results found.")
        return

    # Find first instance of default photo present and appropriate license
    permitted = False
    for record in results:
        photo = record.get('default_photo')
        photo = {} if photo is None else photo
        lic = photo.get('license_code')
        permitted = lic is not None and lic[:3] == 'cc-'
        if permitted:
            break

    if not permitted:
        st.markdown("No photo available.")
    else:
        image_url = photo.get("medium_url")
        st.image(image_url)
        st.markdown(f"Photo by: {photo.get('attribution')}")
