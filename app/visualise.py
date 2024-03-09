from __future__ import annotations

import plotly.graph_objs as go
import plotly.offline as pyo

from utils.setup_env import setup_project_env

# Environment setup
project_dir, config, setup_logs, db_config = setup_project_env()


def plots(df, to_html=False):
    # fig = go.Figure(data=go.Scatter(x=df.index, y=df['value']))
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df['value'], mode='lines', name='value', line=dict(width=0.5)
        )
    )
    fig.update_layout(
        title='My Bloods',
        xaxis_title='Time',
        yaxis_title='Sugar')

    if to_html:
        return pyo.plot(fig, include_plotlyjs=False, output_type='div')
    else:
        fig.show()
