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

idx=pd.IndexSlice
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)

app.title = "FOREX Web Trader"

server = app.server

# Loading historical tick data
tickers = ['AAPL','CVX','FB','TSLA']
iex = 'https://sandbox.iexapis.com/stable'
token='Tpk_f52db219957949dc90226552a6776f50'
params={'token': token,\
                            'symbols':','.join(tickers), \
                            'types':'chart', \
                            'chartLast': 12, \
                            'chartIEXOnly':'true'
                            }
resp=requests.get(iex+'/stock/market/batch',params=params)
d=resp.json()
ticker_pair_data = pd.concat([pd.DataFrame(v) for k,v in d.items()], keys=d)
ticker_pair_data=ticker_pair_data['chart'].apply(pd.Series)
def get_row(ticker):
    data=ticker_pair_data.loc[idx[ticker,:]]
    index = max(data.index.tolist())
    current_row = ticker

    return html.Div(
        children=[
            # Summary
            html.Div(
                id=ticker + "summary",
                className="row summary",
                n_clicks=0,
                children=[
                    html.Div(
                        id=ticker + "row",
                        className="row",
                        children=[
                            html.P(
                                ticker,  # currency pair name
                                id=ticker,
                                className="three-col",
                            ),
                            html.P(
                                data.loc[index,'close'].round(5),  # Bid value
                                id=ticker + "close",
                                className="three-col",
                            ),
                            html.P(
                                data.loc[index,'open'].round(5),  # Ask value
                                id=ticker + "open",
                                className="three-col",
                            ),
                            html.Div(
                                index,
                                id=ticker
                                + "index",  # we save index of row in hidden div
                                style={"display": "none"},
                            ),
                        ],
                    )
                ],
            ),
            # Contents
            html.Div(
                id=ticker + "contents",
                className="row details",
                children=[
                    # Button for buy/sell modal
                    html.Div(
                        className="button-buy-sell-chart",
                        children=[
                            html.Button(
                                id=ticker + "Buy",
                                children="Buy/Sell",
                                n_clicks=0,
                            )
                        ],
                    ),
                    # Button to display currency pair chart
                    html.Div(
                        className="button-buy-sell-chart-right",
                        children=[
                            html.Button(
                                id=ticker + "Button_chart",
                                children="Chart",
                                n_clicks=1
                                if ticker in ["EURUSD", "USDCHF"]
                                else 0,
                            )
                        ],
                    ),
                ],
            ),
        ]
    )
app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in tickers],
        value=tickers[0]
    ),
    html.Div(id='display-value'),
    html.Div(
                    className="div-currency-toggles",
                    children=[
                        html.P(
                            id="live_clock",
                            className="three-col",
                            children=datetime.datetime.now().strftime("%H:%M:%S"),
                        ),
                        html.P(className="three-col", children="close"),
                        html.P(className="three-col", children="open"),
                        html.Div(
                            id="pairs",
                            className="div-bid-ask",
                            children=[
                                get_row(pair)
                                for pair in tickers
                            ],
                        ),
                    ],
                ),
    html.Div(
            className="nine columns div-right-panel",
            children=[
                # Top Bar Div - Displays Balance, Equity, ... , Open P/L
                html.Div(
                    id="top_bar", className="row div-top-bar", children=get_top_bar()
                ),
                # Charts Div
                html.Div(
                    id="charts",
                    className="row",
                    children=[chart_div(pair) for pair in currencies],
                ),
                # Panel for orders
                html.Div(
                    id="bottom_panel",
                    className="row div-bottom-panel",
                    children=[
                        html.Div(
                            className="display-inlineblock",
                            children=[
                                dcc.Dropdown(
                                    id="dropdown_positions",
                                    className="bottom-dropdown",
                                    options=[
                                        {"label": "Open Positions", "value": "open"},
                                        {
                                            "label": "Closed Positions",
                                            "value": "closed",
                                        },
                                    ],
                                    value="open",
                                    clearable=False,
                                    style={"border": "0px solid black"},
                                )
                            ],
                        ),
                        html.Div(
                            className="display-inlineblock float-right",
                            children=[
                                dcc.Dropdown(
                                    id="closable_orders",
                                    className="bottom-dropdown",
                                    placeholder="Close order",
                                )
                            ],
                        ),
                        html.Div(id="orders_table", className="row table-orders"),
                    ],
                ),
            ],
        ),
])
# Callback to update live clock
# @app.callback(Output("live_clock", "children"), [Input("interval", "n_intervals")])
# def update_time(n):
#     return datetime.datetime.now().strftime("%H:%M:%S")

@app.callback(Output('display-value', 'children'),
                [Input('dropdown', 'value')])
def display_value(value):
    resp=requests.get(iex+'/stock/market/batch',params=params)
    d=resp.json()
    currency_pair_data = pd.concat([pd.DataFrame(v) for k,v in d.items()], keys=d)
    currency_pair_data=currency_pair_data['chart'].apply(pd.Series)
    c='Close Price: {}'.format(d[value]['chart'][0]['close'])
    return c#'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)