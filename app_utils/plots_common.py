import plotly.express as px
import plotly.colors as pc


PRIMARY = pc.sequential.Darkmint_r[2]
SECONDARY = pc.qualitative.Set2[1]
DIVERGING_PALETTE = pc.diverging.Portland


def continuous_colors(n, reverse=False):
    if reverse:
        return pc.sample_colorscale(px.colors.sequential.Darkmint_r, [i / (n - 1) for i in range(n)])
    else:
        return pc.sample_colorscale(px.colors.sequential.Darkmint, [i / (n - 1) for i in range(n)])


def ratings_axis_args(tickvals=list(range(5)), stack=False):
    letters = ['EDCBA'[v] for v in tickvals]
    if stack:
        ticktext = [f"{v}<br>({l})" for v, l in zip(tickvals, letters)]
    else:
        ticktext = [f"{v} ({l})" for v, l in zip(tickvals, letters)]
    return tickvals, ticktext