from __future__ import annotations

import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo


def access_and_store(data):
    """Access the data and store it in a pandas dataframe"""

    quotes = data['chart']['result'][0]['indicators']['quote'][0]
    timestamps = data['chart']['result'][0]['timestamp']

    df = pd.DataFrame(quotes)
    dt_series = pd.to_datetime(timestamps, unit='s')
    df.index = dt_series

    for col in df.columns:
        df[col] = df[col].ffill()

    return df


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

    # df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    # df.set_index('Timestamp', inplace=True)
    # df = df.sort_index()

    # print("Combined DataFrame with GraphData and GlucoseMeasurement:")
    # print(glucose_measurement_df)

    # print(combined_values_df)
