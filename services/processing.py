from __future__ import annotations

from datetime import datetime

import plotly.graph_objs as go
import plotly.offline as pyo


def process_timestamps(data):
    """Convert timestamps to datetime objects."""
    timestamp_format = '%m/%d/%Y %I:%M:%S %p'
    for item in data:
        item['Timestamp'] = datetime.strptime(
            item['Timestamp'], timestamp_format)
        item['FactoryTimestamp'] = datetime.strptime(
            item['FactoryTimestamp'], timestamp_format)


def plotting(df, to_html=False):
    fig = go.Figure(data=go.Scatter(x=df.index, y=df['close']))
    fig.update_layout(
        title='Stock Data for NVDA',
        xaxis_title='Time',
        yaxis_title='Closing Price')

    if to_html:
        return pyo.plot(fig, include_plotlyjs=False, output_type='div')
    else:
        fig.show()
