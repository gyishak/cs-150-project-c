from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd

from helper import house_price_table, income_table, trans_table, ele_table, county_house_tab, food_tab

app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY, dbc.icons.FONT_AWESOME])
df = pd.read_csv("assets/data1.csv")
dataHouse=pd.read_csv("assets/homeprices.csv")
dataTransp=pd.read_csv("assets/transportation.csv")
electric=pd.read_csv("assets/electric.csv")
county_house=pd.read_csv("assets/county_house_price.csv")

data1 = pd.read_csv("assets/homeprices.csv").to_dict('records')
data2 = pd.read_csv("assets/data1.csv").to_dict('records')
data3= pd.read_csv("assets/transportation.csv").to_dict('records')
data4 = pd.read_csv("assets/electric.csv").to_dict('records')
data6=pd.read_csv("assets/county_house_price.csv").to_dict('records')

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
         [House Prices Source](https://fred.stlouisfed.org/series/NYSTHPI)
         [Gasoline Prices Source] ( https://www.nyserda.ny.gov/Energy-Prices/Motor-Gasoline/Monthly-Average-Motor-Gasoline-Prices#NY-Statewide )
         [Electricity Prices Source](https://www.nyserda.ny.gov/Energy-Prices/Electricity/Monthly-Avg-Electricity-Residential)
         [CPI Food and Beverages in NY](https://fred.stlouisfed.org/series/CUURA101SAF)
         [CPI Food and Beverages in US] (https://fred.stlouisfed.org/series/CPIUFDSL)
         [County House Prices] (https://www.tax.ny.gov/research/property/assess/sales/resmedian.htm)
         
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
       html.Div([house_price_table, income_table, trans_table, ele_table, county_house_tab, food_tab]),
   ],
   className="mt-4",
)