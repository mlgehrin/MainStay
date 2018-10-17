
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web # requires v0.6.0 or later
from datetime import datetime


app = dash.Dash(__name__)
server = app.server

nsdq = pd.read_csv('NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)
options = []
for tic in nsdq.index:
    options.append({'label':'{} {}'.format(tic,nsdq.loc[tic]['Name']), 'value':tic})

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.Div([
        html.Div([
            html.H3('Select stock symbols:', style={'paddingRight':'30px'}),
            dcc.Dropdown(
                id='my_ticker_symbol',
                options=options,
                value=['TSLA'],
                multi=True
            )
        ], 
            #style={'display':'inline-block', 'verticalAlign':'top', 'width':'30%'},
            #className = "four column"
        ),
        html.Div([
            html.H3('Select start and end dates:'),
            dcc.DatePickerRange(
                id='my_date_picker',
                min_date_allowed=datetime(2015, 1, 1),
                max_date_allowed=datetime.today(),
                start_date=datetime(2018, 1, 1),
                end_date=datetime.today()
            )
        ], 
            #style={'display':'inline-block'},
            className = "four column"),
        html.Div(
            html.Button(
                id='submit-button',
                n_clicks=0,
                children='Submit',
                style={'fontSize':24, 'marginLeft':'30px', 'marginTop': '5px'}
            ),  
            #style={'display':'inline-block'},
            className = "four column")],
        className = "row"),
    html.Div(
        dcc.Graph(
            id='my_graph',
            figure={
                'data': [
                    {'x': [1,2], 'y': [3,1]}
        ]}),
        className="modal-content",
        style={"textAlign": "center", "border": "1px solid #C8D4E3"}
    ),
    
    html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",rel="stylesheet"),
    html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css", rel="stylesheet")
])
@app.callback(
    Output('my_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('my_ticker_symbol', 'value'),
    State('my_date_picker', 'start_date'),
    State('my_date_picker', 'end_date')])
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    traces = []
    for tic in stock_ticker:
        df = web.DataReader(tic,'iex',start,end)
        traces.append({'x':df.index, 'y': df.close, 'name':tic})
    fig = {
        'data': traces,
        'layout': {'title':', '.join(stock_ticker)+' Closing Prices'}
    }
    return fig

if __name__ == '__main__':
    app.run_server()
