from dash import Dash, dcc, html, Input, Output, callback_context
import dash_bootstrap_components as dbc
import pandas as pd

from Learn import learn_card
from Play import input_groups, time_period_card, time_period_data
from Results import house_price_card, footer
from helper import backtest, backCap, backSec, backBar, make_line_chart, secondLine, make_bar, thirdChart

app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY, dbc.icons.FONT_AWESOME])
df = pd.read_csv("assets/data1.csv")
dataHouse=pd.read_csv("assets/homeprices.csv")
dataTransp=pd.read_csv("assets/transportation.csv")
electric=pd.read_csv("assets/electric.csv")
food=pd.read_csv("assets/new_food.csv")
county_house=pd.read_csv("assets/county_house_price.csv")


data1 = pd.read_csv("assets/homeprices.csv").to_dict('records')
data2 = pd.read_csv("assets/data1.csv").to_dict('records')
data3= pd.read_csv("assets/transportation.csv").to_dict('records')
data4 = pd.read_csv("assets/electric.csv").to_dict('records')
data5= pd.read_csv("assets/new_food.csv").to_dict('records')
data6=pd.read_csv("assets/county_house_price.csv").to_dict('records')


MAX_YEAR=df.Year.max()
MIN_YEAR=df.Year.min()
START_YR=1990


foodPrice=dbc.InputGroup([
  dbc.InputGroupText("Enter current monthly food price (2024):"),
  dbc.Input(
      id="foodPrice",
      placeholder=0,
      type="number",
      min=0,
  ),
],
  className="mt",
)
myincome=dbc.InputGroup([
  dbc.InputGroupText("Enter Your Income"),
  dbc.Input(
      id="myincome",
      placeholder=0,
      type="number",
      min=0,
  ),
],
  className="mt",
)
housePrice=dbc.InputGroup([
  dbc.InputGroupText("Enter how much you are willing to spend on a house (2023) to see what NY counties fit that range:"),
  dbc.Input(
      id="housePrice",
      placeholder=0,
      type="number",
      min=0,
  ),
],
  className="mt",
)

enter_in=html.Div(
  [
        myincome, foodPrice, housePrice
  ],
  className="mt-4 p-4",
)

myNewYork_card = dbc.Card(
  [
      html.H4(
          "My New York Life:",
          className="card-title",
      ),
      dcc.Store(id="enter_ins"),
  ],
  body=True,
  className="mt-4",
)
