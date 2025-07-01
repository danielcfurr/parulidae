import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from .plots_common import PRIMARY, SECONDARY, list_to_markdown_bullets


def recordings_by_month(recordings: pd.DataFrame, species: str):
    dat = recordings.copy()
    dat['month_num'] = dat['date'].dt.month
    dat['month_name'] = dat['date'].dt.strftime('%b')

    # Create an index to guarantee no missing months
    group_cols = ['month_num', 'month_name']
    expected = dat[group_cols].drop_duplicates().sort_values('month_num')
    expected_index = pd.Index(expected)

    dat = dat.loc[dat['en'] == species]

    recording_counts_by_month = (
        dat.groupby(group_cols).size().rename('recordings').reindex(expected_index).fillna(0).to_frame().reset_index()
    )
    recording_counts_by_month.columns = group_cols + ['recordings']

    fig = px.bar(
        recording_counts_by_month,
        x='month_num',
        y='recordings',
        labels={'month_num': 'Month of recording', 'recordings': 'Number of recordings'},
        title=f'Number of recordings by month (summing across years)',
        color_discrete_sequence=[PRIMARY]
    )

    fig.update_xaxes(
        tickmode='array',
        tickvals=expected['month_num'],
        ticktext=expected['month_name'],
        tickangle=45
    )

    return fig


def recordings_by_year(recordings: pd.DataFrame, species: str):
    dat = recordings.loc[recordings['en'] == species].copy()
    dat['year'] = dat['date'].dt.year

    expected_years = np.arange(2015, 2025, 1)

    recording_counts_by_year = (
        dat.groupby('year').size().rename('recordings').reindex(expected_years).fillna(0).to_frame().reset_index()
    )
    recording_counts_by_year.columns = ['year', 'recordings']

    fig = px.line(
        recording_counts_by_year,
        x='year',
        y='recordings',
        labels={'year': 'Year of recording', 'recordings': 'Number of recordings'},
        title=f'Number of recordings by year',
        color_discrete_sequence=[PRIMARY],
        markers=True
    )

    fig.update_xaxes(
        dtick="M12",
        tickangle=45
    )

    fig.update_yaxes(rangemode="tozero")

    return fig


def box_compare(recordings: pd.DataFrame, species:str, column_name: str, column_title: str):
    dat = recordings.copy()
    dat['selected'] = dat['en'] == species
    dat['selected_label'] = 'All other species'
    dat.loc[dat['selected'], 'selected_label'] = species

    ratings_summary_by_species = (
        dat.groupby(['selected', 'selected_label', 'en'])['q_num'].agg(['mean', 'size']).reset_index()
    )
    ratings_summary_by_species['jitter'] = np.random.uniform(-.2, .2, len(ratings_summary_by_species))
    ratings_summary_by_species.loc[ratings_summary_by_species['selected'], 'jitter'] = 0

    fig = go.Figure()

    fig.add_trace(go.Box(
        x=ratings_summary_by_species[column_name],
        y=[0] * len(ratings_summary_by_species),
        orientation='h',
        name="Size",
        boxpoints=False,
        marker_color='lightgray',
        line=dict(width=1),
        showlegend=False
    ))

    sub = ratings_summary_by_species.loc[ratings_summary_by_species['selected']]
    hovertext = [f"{sp}<br>{column_title}: {x}" for sp, x in zip(sub['en'], sub['size'])]
    fig.add_trace(go.Scatter(
        x=sub[column_name],
        y=sub['jitter'],
        mode='markers',
        marker=dict(color=SECONDARY, size=12, symbol='diamond'),
        name=species,
        showlegend=True,
        hovertext=hovertext,
        hoverinfo='text',
    ))

    sub = ratings_summary_by_species.loc[~ratings_summary_by_species['selected']]
    hovertext = [f"{sp}<br>{column_title}: {x}" for sp, x in zip(sub['en'], sub['size'])]
    fig.add_trace(go.Scatter(
        x=sub[column_name],
        y=sub['jitter'],
        mode='markers',
        marker=dict(color=PRIMARY, size=6, opacity=1),
        name="Other warblers",
        showlegend=True,
        hovertext=hovertext,
        hoverinfo='text',
    ))

    fig.update_layout(
        title=f"{column_title} versus other warblers",
        #title_x=0.5,
        xaxis_title=column_title,
        yaxis=dict(title="", showticklabels=False, zeroline=False, ticks=''),
        template="simple_white",
        hovermode="closest",
        legend=dict(
            title="",
            orientation="h",
            yanchor="bottom",
            y=0.0,
        )
    )

    return fig


def recordings_versus_other_species(recordings: pd.DataFrame, species:str):
    return box_compare(recordings, species, column_name='size', column_title='Number of recordings')


def ratings_versus_other_species(recordings: pd.DataFrame, species:str):
    return box_compare(recordings, species, column_name='mean', column_title='Average rating')


def highlights(recordings: pd.DataFrame, species:str):
    dat = recordings.copy().loc[recordings['en'] == species]

    n_recordings = len(dat)
    n_contributors = dat['rec'].nunique()
    first_upload = dat['uploaded'].min().date()
    last_upload = dat['uploaded'].max().date()

    facts = [
      f'Total recordings: {n_recordings}',
      f'Total contributors: {n_contributors}',
      f'First uploaded recording: {first_upload}',
      f'Last uploaded recording: {last_upload}'
    ]

    return list_to_markdown_bullets(facts)
