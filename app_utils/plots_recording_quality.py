import pandas as pd
import plotly.express as px
from .plots_common import PRIMARY, DIVERGING_PALETTE, ratings_axis_args


def device_summary(recordings: pd.DataFrame):
    recordings_counts = recordings['dvc'].value_counts()
    selected_devices = recordings_counts.index[recordings_counts >= 10]

    devices = (
        recordings
        .loc[recordings['dvc'].isin(selected_devices)]
        .groupby('dvc')['q_num']
        .agg(['mean', 'count'])
        .reset_index()
    )

    return devices


def quality_verus_popularity(recordings: pd.DataFrame):
    devices = device_summary(recordings)

    fig = px.scatter(
        devices,
        x='count',
        y='mean',
        hover_name='dvc',
        labels={'count': 'Number of recordings', 'mean': 'Average recording quality'},
        color_discrete_sequence=[PRIMARY],
        title='Quality versus popularity of recording devices'
    )

    best = devices.loc[devices['mean'].idxmax()]
    fig.add_annotation(
        x=best['count'],
        y=best['mean'],
        showarrow=True,
        arrowhead=0,
        text=f"Best quality device:<br>{best['dvc']}")

    common = devices.loc[devices['count'].idxmax()]
    fig.add_annotation(
        x=common['count'],
        y=common['mean'],
        showarrow=True,
        arrowhead=0,
        text=f"Most popular device:<br>{common['dvc']}",
    )

    tickvals, ticktext = ratings_axis_args(stack=False)

    fig.update_yaxes(
        tickmode='array',
        tickvals=tickvals,
        ticktext=ticktext
    )

    return fig


def top_devices_quality(recordings: pd.DataFrame):
    devices = device_summary(recordings)

    fig = px.bar(
        devices.sort_values('mean').tail(5),
        x='mean',
        y='dvc',
        labels={'mean': 'Average recording quality'},
        color_discrete_sequence=[PRIMARY],
        title=f'Top five devices for recording quality',
    )

    tickvals, ticktext = ratings_axis_args(stack=True)
    fig.update_xaxes(
        tickmode='array',
        tickvals=tickvals,
        ticktext=ticktext
    )

    fig.update_yaxes(title=None, automargin=True)

    return fig


def top_devices_popularity(recordings: pd.DataFrame):
    devices = device_summary(recordings)

    fig = px.bar(
        devices.sort_values('count').tail(5),
        x='count',
        y='dvc',
        labels={'count': 'Number of recordings'},
        color_discrete_sequence=[PRIMARY],
        title=f'Top five most popular devices'
    )

    fig.update_yaxes(title=None, automargin=True)

    return fig


def recordings_by_quality(recordings):
    quality_rating_counts = recordings.groupby(['q_num', 'q'], observed=True).size().rename('count').reset_index()

    fig = px.bar(
        quality_rating_counts,
        x='q_num',
        y='count',
        color='q',
        color_discrete_sequence=DIVERGING_PALETTE,
        title="Number of recordings by quality rating",
        labels={'q_num': 'Quality rating', 'count': 'Number of recordings'},
        hover_data={'q': None}
    )

    tickvals, ticktext = ratings_axis_args(stack=False)
    fig.update_xaxes(
        tickmode='array',
        tickvals=tickvals,
        ticktext=ticktext,
        autorange='reversed'
    )

    fig.update_layout(showlegend=False)

    return fig


def quality_by_year(recordings: pd.DataFrame):
    dat = recordings.copy()
    dat['year'] = dat['uploaded'].dt.year
    dat = dat.loc[dat['year'] < dat['year'].max()]

    quality_by_year_counts = dat.groupby('year')['q_num'].mean().to_frame().reset_index()

    fig = px.line(
        quality_by_year_counts,
        x='year',
        y='q_num',
        labels={'year': 'Year', 'q_num': 'Average recording quality'},
        title='Average recording quality by year of upload',
        color_discrete_sequence=[PRIMARY],
        markers=True
    )

    fig.update_xaxes(
        dtick="M12",
        tickangle=45
    )

    tickvals, ticktext = ratings_axis_args(stack=False)
    fig.update_yaxes(
        tickmode='array',
        tickvals=tickvals,
        ticktext=ticktext,
        range=[0, 4]
    )

    return fig
