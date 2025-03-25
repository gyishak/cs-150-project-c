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

learn_text=dcc.Markdown(
    ''' 
Please explore the three graphs:
    
1. House Price Index Overtime
Line graph depicting trend of house price index from 1990 to 2023.
	
2. Income Spanning Overtime
Bar graph depicting income levels across the years from 1990 to 2023.

3. Gasoline and Electricity Prices Overtime
Line graph comparing gasoline prices ($ per gallon) and electricity prices
($ per kilowatt-hour) from 2012 to 2023.
     
  What type trends do you notice regarding the house prices compared to the household
  income? What about the gasoline and electricity prices?


  Use the interactive elements to understand how key time periods, like
  COVID-19, have influenced the fluctuations in home prices, income, gasoline prices,
  and electricity prices.


  Please look through the Results tab to see all the data used for this study.
 
  Thank you!

    
    
    

	
'''
)

# ========= Learn Tab  Components
learn_card = dbc.Card(
    [
        dbc.CardHeader("Hello, New Yorkers!"),
        dbc.CardBody(learn_text),
    ],
)