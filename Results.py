from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

from helper import backtest, backCap, backSec, backBar, make_line_chart, secondLine, make_bar, house_price_table, \
    income_table, trans_table, ele_table

app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY, dbc.icons.FONT_AWESOME])
df = pd.read_csv("assets/data1.csv")
dataHouse=pd.read_csv("assets/homeprices.csv")
dataTransp=pd.read_csv("assets/transportation.csv")
electric=pd.read_csv("assets/electric.csv")


data1 = pd.read_csv("assets/homeprices.csv").to_dict('records')
data2 = pd.read_csv("assets/data1.csv").to_dict('records')
data3= pd.read_csv("assets/transportation.csv").to_dict('records')
data4 = pd.read_csv("assets/electric.csv").to_dict('records')


MAX_YEAR=df.Year.max()
MIN_YEAR=df.Year.min()
START_YR=1990

"""
==========================================================================
Markdown Text
"""

footer = html.Div(
    dcc.Markdown(
        """
         [Household Income Source](https://fred.stlouisfed.org/series/MEHOINUSNYA672N)
         [House Price Source](https://fred.stlouisfed.org/series/NYSTHPI)
         [Gasoline Price Source] ( https://www.nyserda.ny.gov/Energy-Prices/Motor-Gasoline/Monthly-Average-Motor-Gasoline-Prices#NY-Statewide )
         [Electricity Expenditures Source](https://www.nyserda.ny.gov/Energy-Prices/Electricity/Monthly-Avg-Electricity-Residential)
        """
    ),
    className="p-2 mt-5 text-white small",
)



"""
===========================================================================
Results
"""
house_price_card = dbc.Card(
   [
       dbc.CardHeader(""),
       html.Div([house_price_table, income_table, trans_table, ele_table]),
   ],
   className="mt-4",
)