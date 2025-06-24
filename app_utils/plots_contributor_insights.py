import pandas as pd
import numpy as np
import plotly.express as px
from .plots_common import PRIMARY, SECONDARY, DIVERGING_PALETTE, continuous_colors, ratings_axis_args


def cumulative_contributors_by_recording_threshold(recordings: pd.DataFrame):
    recordings_per_contributor = recordings.groupby('rec').size().rename('recordings')
    thresholds = np.arange(1, 50 + 1, 1)

    survival = pd.DataFrame({
        'threshold': thresholds,
        'proportion': [np.mean(recordings_per_contributor >= t) for t in thresholds]
    })

    fig = px.line(
        survival,
        x='threshold',
        y='proportion',
        labels={'threshold': 'Minimum number of recordings', 'proportion': 'Percentage of contributors'},
        title='Percentage of contributors by minimum number of recordings',
        color_discrete_sequence=[PRIMARY],
    )

    def annotate(fig, threshold):
        prop = survival.loc[survival['threshold'] == threshold, 'proportion'].iloc[0]
        text = f'{prop * 100:.0f}% of contributors uploaded <br> {threshold:.0f} or more recordings'
        fig.add_annotation(
            x=threshold, y=prop,
            xanchor='left', yanchor='bottom',
            ax=30, ay=-20,
            text=text,
        )

    annotate(fig, 2)
    annotate(fig, 10)

    fig.update_yaxes(tickformat='.0%', rangemode="tozero")

    return fig


def cumulative_recordings_versus_contributor_percentile(recordings: pd.DataFrame):
    recordings_per_contributor = recordings.groupby('rec').size().rename('recordings')

    rank = recordings_per_contributor.rank(method='first', ascending=False, pct=True)
    total = recordings_per_contributor.sum()
    quantiles = pd.Series(np.linspace(.01, 1, num=100), name='quantile')
    cumulative_share = pd.DataFrame({
        'quantile': quantiles,
        'cum_prop': [recordings_per_contributor[rank <= q].sum() / total for q in quantiles]
    })

    fig = px.line(
        cumulative_share,
        x='quantile',
        y='cum_prop',
        labels={'quantile': 'Percentile of contributors', 'cum_prop': 'Cumulative percentage<br>of recordings'},
        title="Cumulative share of recordings by contributor percentile",
        color_discrete_sequence=[PRIMARY],
    )

    def annotate(fig, quantile):
        cum_prop = cumulative_share.loc[cumulative_share['quantile'] == quantile, 'cum_prop'].iloc[0]
        text = f'Top {quantile * 100:.0f}% of contributors <br> uploaded {cum_prop * 100:.0f}% of all recordings'
        fig.add_annotation(
            x=quantile, y=cum_prop,
            xanchor='left', yanchor='top',
            ax=30, ay=20,
            text=text,
        )

    annotate(fig, .05)
    annotate(fig, .20)

    fig.update_xaxes(tickformat='.0%')
    fig.update_yaxes(tickformat='.0%', rangemode="tozero")

    return fig


def new_returning_by_month(recordings: pd.DataFrame):
    dat = recordings.copy()
    dat['first_upload'] = recordings.groupby('rec')['uploaded'].transform(lambda x: x == np.min(x))
    dat['month'] = dat['uploaded'].dt.to_period('M')

    contributor_status_by_month = dat.groupby(['rec', 'month'])['first_upload'].max()
    contributor_count_by_month = (
        contributor_status_by_month.to_frame().reset_index()
        .groupby(['month', 'first_upload']).size().unstack(fill_value=0)
        .rename({True: 'New contributors', False: 'Returning contributors'}, axis=1)
        .reset_index()
    )
    contributor_count_by_month['month'] = contributor_count_by_month['month'].astype(str)

    fig = px.line(
        contributor_count_by_month,
        x='month',
        y=['Returning contributors', 'New contributors'],
        labels={'month': 'Month', 'value': 'Number of contributors', 'variable': 'Contributor type'},
        color_discrete_sequence=[PRIMARY, SECONDARY],
        title='Number of new and returning contributors by month'
    )

    fig.update_xaxes(
        dtick="M12",
        tickangle=45
    )

    return fig


def contributor_retention(recordings: pd.DataFrame):
    dat = recordings.copy()

    tenure_in_days = dat.groupby('rec')['uploaded'].apply(lambda x: np.max(x) - np.min(x)).dt.days

    days = pd.Series(np.arange(0, 1005, 5), name='days')

    plot_df = pd.DataFrame({
        'days': days,
        'survival_prop': [np.mean(tenure_in_days >= d) for d in days]
    })

    fig = px.line(
        plot_df,
        x='days',
        y='survival_prop',
        title='Contributor retention over time',
        labels={'days': 'Days since first upload', 'survival_prop': 'Percentage of <br> returning contributors'},
        color_discrete_sequence=[PRIMARY],
    )

    def annotate(fig, days):
        prop = plot_df.loc[plot_df['days'] == days, 'survival_prop'].iloc[0]
        text = f'{prop * 100:.0f}% of contributors uploaded<br> again after {days:.0f} days'
        fig.add_annotation(
            x=days, y=prop,
            xanchor='left', yanchor='bottom',
            ax=30, ay=-20,
            text=text,
        )

    annotate(fig, 5)
    annotate(fig, 365)

    fig.update_yaxes(tickformat='.0%', rangemode="tozero")

    return fig
