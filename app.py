import datetime
import dash
from dash import dcc
#import dash_core_components as dcc
#import dash_html_components as html
from dash import html
from dash.dependencies import Input, Output
from dash import html
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
#from alpha_vantage.timeseries import TimeSeries


#Constants to download data
START = "2018-01-01"
#TODAY = date.today().strftime("%Y-%m-%d")
TODAY = datetime.datetime.now().strftime("%Y-%m-%d")
FTODAY=datetime.datetime.now().strftime("%m-%d-%Y")
API_KEY = 'T6X62ZNC78VB55YK'
IMGE = 'assets/nft.PNG'
# ccys = ["BTC", "ETH", "USDT", "USDC","BNB","XRP", "ADA", "BUSD", "SOL", "DOGE"]

#Grabbing all tick symbols from a csv
tick_data = pd.read_csv('assets/c_ticker.csv')
tick_df = pd.DataFrame(tick_data)
#tick_df = tick_df.drop('Company Name',axis=1)
ticks = tick_df['Symbol'].to_list()

#Helper function to load historical daily data
def load_daily(ticker):
    """
    Loads the dataset for the selected ticker
    """
    data = yf.download(ticker,START,TODAY)
    data.reset_index(inplace=True)
    return data 

#Initializing dash app
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
                html.Div(children=[
                    html.H2(children='Cryptocurrency Latest News Dashboard'),
                    html.H4(children='Data from 01-01-2018 thru '+FTODAY, style={'marginTop': '-15px', }),
                    ], style={'textAlign': 'center'}),

                html.Div(children=[
                    html.Div(children=[
                        html.Label('Select ticker:', style={'paddingTop': '2rem'}),
                        dcc.Dropdown(
                                id = 'ticker-drop',
                                options = [{'label': i,'value':i} for i in ticks ],
                                multi = False,
                                value = 'ETH-USD',
                                className= "mb-3"
                            ),
                    ],),
                    html.Hr(),                
                ],className="three columns",
                style={'padding':'2rem', 'margin':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem'} ),
                               
# Number statistics & OHLC each day
            html.Div(children= [ 
                html.Div(children=[
                    #Stats box 
                    html.Div(children=[
                        html.Div(children=[
                                    html.H3(id='open-sb', style={'fontWeight': 'bold'}),
                                    html.Label('Opening price in USD($)', style={'paddingTop': '.3rem'}),
                        ], className="two columns number-stat-box"),
                    
                        html.Div(children=[
                                    html.H3(id='high-sb', style={'fontWeight': 'bold', 'color': '#f73600'}),
                                    html.Label('Highest price in USD($)', style={'paddingTop': '.3rem'}),
                        ], className="two columns number-stat-box"),

                        html.Div(children=[
                                    html.H3(id='low-sb', style={'fontWeight': 'bold', 'color': '#00aeef'}),
                                    html.Label('Lowest price in USD($)', style={'paddingTop': '.3rem'}),
                        ], className="two columns number-stat-box"),
                        
                        html.Div(children=[
                                    html.H3(id='close-sb', style={'fontWeight': 'bold', 'color': '#a0aec0'}),
                                    html.Label('Closing price in USD($)', style={'paddingTop': '.3rem'}),
                        ], className="two columns number-stat-box"),
                        
                        html.Div(children=[
                                    html.H3(id='volume-sb', style={'fontWeight': 'bold', 'color': '#0fa'}),
                                    html.Label('Volume of shares', style={'paddingTop': '.3rem'}),
                        ], className="three columns number-stat-box")],
                        style= {'margin':'1rem', 'display': 'flex', 'justify-content': 'space-between', 'width': '100%', 'flex-wrap': 'wrap'}),

                    #OH & LC Graphs
#                    html.Div(children=[
#                       dcc.Graph(id='open-close-fig')
#                    ], className="six columns", style={'padding':'.3rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'white', }),
#                    
#                    html.Div(children=[
#                        dcc.Graph(id='high-low-fig')
#                    ], className="six columns", style={'padding':'.3rem', 'marginTop':'1rem', 'marginLeft':'3rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'white', }),
                   
                ], className="twelve columns", style={'backgroundColor': '#f2f2f2', 'margin': '1rem'})
            ], style={'display': 'flex', 'flex-wrap': 'wrap'}),      
        html.Div(children=[ 
        # OHLC
            html.Div(children=[
                dcc.Graph(id='ohlc')
            ], className="twleve columns", style={'padding':'2rem',  'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': '#31353b'})        
        ], style={'margin': '1rem', })            
                    
], style={'padding': '2rem'})

#--------------------------
#Callbacks

@app.callback(
    #Output('open-close-fig','figure'),
    #Output('high-low-fig','figure'),
    Output('open-sb','children'),
    Output('high-sb','children'),
    Output('low-sb','children'),
    Output('close-sb','children'),
    Output('volume-sb','children'),
    [Input('ticker-drop','value')]
)
def open_close_graph(value):
    """
    This callback returns a open/close & high/low graph along with the stats for the statbox 
    based on the selected ticker
    """
    #data = load_daily(value)
    #stats = data.tail(1)
    #op = stats['open']
    #cl = stats['close']
    #hg = stats['high']
    #lw = stats['low']
    #vol = stats['volume']
    df = load_daily(value)
    df=df.tail(1)
    op=df['Open'].round(0)
    hg=df['High'].round(0)
    lw=df['Low'].round(0)
    cl=df['Close'].round(0)
    vol=df['Volume'].round(0)
    return op, hg, lw, cl, vol


@app.callback(
    Output('ohlc','figure'),
    Input('ticker-drop','value')
)
def ohlc_graph(value):
    """
    This callback generates an OHLC chart based on the selected tick 
    """
    df = load_daily(value)

    fig = go.Figure(data=[go.Ohlc(
        x=df['Date'],
        open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'],
        increasing_line_color= 'cyan', decreasing_line_color= '#33ff00'
    )])
    fig.layout.update(title=f'OHLC chart for {value} from 01-01-2018 thru '+FTODAY, 
        title_font_size= 23,
        xaxis_title='Date',
        yaxis_title= 'Price in USD($)')
    fig.layout.plot_bgcolor = '#31353b'
    fig.layout.paper_bgcolor = '#31353b'
    fig.update_layout(
        font_color= '#FFFFFF'
    )
    return fig



if __name__ == '__main__':
    app.run_server(debug=True, )