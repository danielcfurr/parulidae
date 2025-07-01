import folium
from folium.plugins import HeatMap
import pandas as pd


def map_heat(recordings: pd.DataFrame, map_args: dict = None, heatmap_args: dict = None):
    if map_args is None:
        map_args = dict(location=[39, -97], zoom_start=4)

    if heatmap_args is None:
        heatmap_args = dict(radius=20)

    m = folium.Map(**map_args)

    heat_data = [(row['lat'], row['lon']) for _, row in recordings.iterrows()]

    HeatMap(heat_data, **heatmap_args).add_to(m)

    return m


def map_recordings(recordings: pd.DataFrame, species: str, map_args: dict = None):
    subset = recordings.loc[recordings['en'] == species]

    if map_args is None:
        map_args = dict(
            location=[39, -97],
            zoom_start=4,
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr='Esri'
        )

    m = folium.Map(**map_args)

    for idx, row in subset.iterrows():
        html = (
            f"""
            Contributor: {row['rec']} <br>
            Location: {row['loc'][:50]} <br>
            Recorded: {row['date'].date()} <br>
            Uploaded: {row['uploaded'].date()} <br>
            License:  {row['lic']} <br>
            <br>
            <a href={row['url']} target="_blank" rel="noopener noreferrer">Link</a>
            """
        )
        folium.Marker(
            location=[row['lat'], row['lon']],
            #tooltip=idx,
            tooltip=html,
            popup=html,
        ).add_to(m)

    return m
