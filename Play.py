from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

from helper import backtest, backCap, backSec, backBar, make_line_chart, secondLine, make_bar

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
===========================================================================
Play
"""
start_year=dbc.InputGroup([
  dbc.InputGroupText("Start Year"),
  dbc.Input(
      id="start_years",
      placeholder=f"min {MIN_YEAR} max {MAX_YEAR}",
      type="number",
      min=MIN_YEAR,
      max=MAX_YEAR,
      value=START_YR,
  ),
],
  className="mt",
)
start_amount = dbc.InputGroup(
  [
      dbc.InputGroupText("Start Amount $"),
      dbc.Input(
          id="starting_amount",
          placeholder="Min $10",
        disabled=True,
          type="number",
          min=10,
          value=24.7,
      ),
  ],
  className="mb",
)
number_of_years = dbc.InputGroup(
  [
      dbc.InputGroupText("Number of Years:"),
      dbc.Input(
          id="planning_time",
          placeholder="# yrs",
          type="number",
          min=1,
          value=MAX_YEAR - START_YR + 1,
      ),
  ],
  className="mb-3",
)

input_groups=html.Div(
  [
        start_amount, start_year, number_of_years
  ],
  className="mt-4 p-4",
)

time_period_data = [
  {
      "label": f"2020-2023: COVID-19 & Great Financial Crisis to {MAX_YEAR}",
      "start_yr": 2020,
      "planning_time": 3,
  },
  {
      "label": "2007-2009: The Great Recession",
      "start_yr": 2007,
      "planning_time": 2,
  },
  {
       "label": "1999-2010: The decade including 2000 Dotcom Bubble peak",
       "start_yr": 1999,
       "planning_time": 11,
  },
  {
      "label": "1990-1999: The 90's",
      "start_yr": 1990,
      "planning_time": 10,
  },
  {
      "label": "1985-1989: The 80's",
      "start_yr": 1985,
      "planning_time": 4,
  },
  {
      "label": f"{MIN_YEAR}-{MAX_YEAR}",
      "start_yr": "1984",
      "planning_time": MAX_YEAR - MIN_YEAR ,
  },
]

time_period_card = dbc.Card(
  [
      html.H4(
          "Select a time period:",
          className="card-title",
      ),
      dcc.Store(id="time_periods"),
      dbc.RadioItems(
          id="time_period",
          options=[
              {"label": period["label"], "value": i}
              for i, period in enumerate(time_period_data)
          ],
          value=0,
          labelClassName="mb-2",
      ),
      html.Div(id='times'),
  ],
  body=True,
  className="mt-4",
)

