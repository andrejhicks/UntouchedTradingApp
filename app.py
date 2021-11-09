# -*- coding: utf-8 -*-
import json
import base64
import datetime
import requests
import pathlib
import math
import pandas as pd
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import chart_studio.plotly as py
import plotly.graph_objs as go

from dash.dependencies import Input, Output, State
from plotly import tools


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)

app.title = "FOREX Web Trader"

server = app.server

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

# Loading historical tick data
currency_pair_data = {
    "EURUSD": pd.read_csv(
        DATA_PATH.joinpath("EURUSD.csv.gz"), index_col=1, parse_dates=["Date"]
    ),
    "USDJPY": pd.read_csv(
        DATA_PATH.joinpath("USDJPY.csv.gz"), index_col=1, parse_dates=["Date"]
    ),
    "GBPUSD": pd.read_csv(
        DATA_PATH.joinpath("GBPUSD.csv.gz"), index_col=1, parse_dates=["Date"]
    ),
    "USDCHF": pd.read_csv(
        DATA_PATH.joinpath("USDCHF.csv.gz"), index_col=1, parse_dates=["Date"]
    ),
}

app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value')
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
                [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)