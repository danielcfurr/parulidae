import pandas as pd
import plotly.express as px
from .plots_common import PRIMARY, SECONDARY, list_to_markdown_bullets


def uploads_by_month_year(monthly: pd.DataFrame):
    dat = monthly.copy()
    dat['Data'] = "Observed"
    dat.loc[dat['forecasted'], 'Data'] = "Forecasted"

    fig = px.line(
        dat,
        x='month',
        y='uploads',
        color='Data',
        color_discrete_sequence=[PRIMARY, SECONDARY],
        labels={'month': 'Month', 'uploads': 'Number of uploads'},
        title="Monthly number of uploaded recordings"
    )

    fig.update_xaxes(
        dtick="M12",
        tickangle=45
    )

    return fig


def uploads_by_month(monthly: pd.DataFrame):
    dat = monthly.copy()
    dat = dat.loc[~dat['forecasted']]
    dat = dat.iloc[:-1]

    dat['date'] = dat['month'].copy()
    dat['month'] = dat['date'].dt.month
    dat['month_name'] = dat['date'].dt.strftime('%b')

    monthly_uploads = dat.groupby(['month', 'month_name'])['uploads'].sum().to_frame().reset_index()

    month_names = dat[['month', 'month_name']].drop_duplicates()

    fig = px.bar(
        monthly_uploads,
        x='month',
        y='uploads',
        color_discrete_sequence=[PRIMARY],
        labels={'month': 'Month', 'year': 'Year', 'uploads': 'Uploads across years'},
        title='Number of monthly uploads across years'
    )

    fig.update_xaxes(
        tickmode='array',
        tickvals=month_names['month'],
        ticktext=month_names['month_name'],
        tickangle=45
    )

    return fig


def uploads_by_year(recordings: pd.DataFrame):
    dat = recordings.copy()

    yearly_uploads = dat.set_index('uploaded').resample('YE').size().iloc[:-1]

    yearly_uploads_df = pd.DataFrame({
        'uploads': yearly_uploads,
        'year': yearly_uploads.index.year
    })

    fig = px.line(
        yearly_uploads_df,
        x='year',
        y='uploads',
        labels={'year': 'Year', 'uploads': 'Number of uploads'},
        title='Number of uploads by year',
        color_discrete_sequence=[PRIMARY],
        markers=True
    )

    fig.update_xaxes(
        dtick="M12",
        tickangle=45
    )

    fig.update_yaxes(rangemode="tozero")

    return fig


def uploads_by_species(recordings: pd.DataFrame):

    recordings_per_species = (
        recordings
        .groupby('en')
        .size()
        .rename('recordings')
        .sort_values()
        .reset_index()
    )

    fig = px.bar(
        recordings_per_species,
        x='recordings', y='en',
        orientation='h',
        color_discrete_sequence=[PRIMARY],
        labels={"recordings": "Number of Recordings"},
        title="Number of recordings by species"
    )

    fig.update_coloraxes(showscale = False)

    fig.update_yaxes(title=None, automargin=True)

    return fig


def highlights(recordings: pd.DataFrame):
    n_recordings = len(recordings)
    n_contributors = recordings['rec'].nunique()
    n_species = recordings['en'].nunique()
    first_upload = recordings['uploaded'].min().date()
    last_upload = recordings['uploaded'].max().date()

    facts = [
      f'Total recordings: {n_recordings}',
      f'Total contributors: {n_contributors}',
      f'Total species: {n_species}',
      f'First uploaded recording: {first_upload}',
      f'Last uploaded recording: {last_upload}'
    ]

    return list_to_markdown_bullets(facts)
