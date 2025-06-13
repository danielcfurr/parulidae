import folium
from folium.plugins import HeatMap
import pandas as pd


def map_heat(recordings_dataframe: pd.DataFrame, map_args: dict = None, heatmap_args: dict = None):
    if map_args is None:
        map_args = dict(location=[39, -97], zoom_start=4)

    if heatmap_args is None:
        heatmap_args = dict(radius=20)

    m = folium.Map(**map_args)

    heat_data = [(row['lat'], row['lon']) for _, row in recordings_dataframe.iterrows()]

    HeatMap(heat_data, **heatmap_args).add_to(m)

    return m


def map_recordings(recordings_dataframe: pd.DataFrame, map_args: dict = None):
    if map_args is None:
        map_args = dict(
            location=[39, -97],
            zoom_start=4,
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr='Esri'
        )

    m = folium.Map(**map_args)

    for idx, row in recordings_dataframe.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            tooltip=idx,
            popup=idx
        ).add_to(m)

    return m
