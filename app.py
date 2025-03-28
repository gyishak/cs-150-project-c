from dash import Dash, dcc, html, Input, Output, callback_context
import dash_bootstrap_components as dbc
import pandas as pd

from Learn import learn_card
from Play import input_groups, time_period_card, time_period_data
from Results import house_price_card, footer
from helper import backtest, backCap, backSec, backBar, make_line_chart, secondLine, make_bar, thirdChart, make_bar2, \
    return_dataset, food_pric_calc, electric_price, find_count
from mynewyork import myNewYork_card, myincome, housePrice, foodPrice

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

"""
===========================================================================
App Layout
"""

app.layout = dbc.Container([
  dbc.Row(
      dbc.Col([
          html.H1([
              "Cost of Living in New York"],
              className="text-center bg-primary text-white p-2",
          ),
        html.H2([
                    "Grace Yishak CS-150"],
                    className="text-center bg-secondary text-white p-2",
               ),
          ],
      )
  ),
  dbc.Row(
      [
          dbc.Tabs([
              dbc.Tab([learn_card], tab_id="tab1", label="Learn"),

    dbc.Tab([input_groups, time_period_card,
           dcc.Graph(id="bar_chart",figure=make_bar(df),className="pb-4"),
           dcc.Graph(id="returns_chart", figure=make_line_chart(dataHouse),className="pb-4"),
           dcc.Graph(id="line_second", figure=secondLine(electric, dataTransp),className="pb-4")
           ],
          tab_id="tab-2", label="Play", className="pb-4",),
dbc.Tab([myNewYork_card, myincome,
            dbc.Row([
            dbc.Col([
                dcc.Graph(id="bar2", figure=make_bar2(df, myincome), className="pb-4"),
                housePrice,
                html.Div(id="county_incomes", children="My Counties:"),
                foodPrice,
                html.Div(id="food_price", children="Monthly Cost"),
                #dcc.Input(id="month_food", type="number"),
                html.Div(id="electric_price_month", children="Monthy Cost"),
            ])
                     ]),
                ],
          tab_id="tab-4", label="Your New York Life"),
    dbc.Tab([house_price_card],
          tab_id="tab-3", label="Results"),
]),
    ],
    id="tabs",

    ),
    footer
      ],
      className="ms-1",
      fluid=True,
  )


"""
===========================================================================
Callback
"""

@app.callback(
    Output("county_incomes", "children"),
    Input("housePrice", "value"),
    allow_duplicate=True,
)
def find_county(initial_house):
    if initial_house is None:
        return ""
    ctx = callback_context
    my_counts=find_count(county_house, initial_house)
    return ', '.join(my_counts)



@app.callback(
    Output("food_price", "children"),
    Output("electric_price_month", "children"),
    Input("foodPrice", "value"),

    allow_duplicate=True,
)
def update_food(foodPrice):
  ctx = callback_context
  month_electric = electric_price(electric)
  month_electric= f"Monthly Electricity Price Per Month in 2023: ${month_electric:.2f}"
  if foodPrice is None:
      return  f"Monthly Food Price in NY Region for 2024: {0}", month_electric

  x=food_pric_calc(food, foodPrice)
  x= f"Monthly Food Price in NY Region for 2024: ${x:.2f}"
  return  x,month_electric


@app.callback(
    Output("bar2", "figure"),
    Input("myincome", "value"),
    allow_duplicate=True,
)
def update_income(myincome):
  ctx = callback_context
  myincome= 0 if myincome is None else myincome
  ds=return_dataset(df)
  line_fig=make_bar2(ds, myincome)

  return line_fig

@app.callback(
  Output("planning_time", "value"),
  Output("start_years", "value"),
  Output("time_period", "value"),
  Input("planning_time", "value"),
  Input("start_years", "value"),
  Input("time_period", "value"),
)
def update_time_period(planning_time, start_yr, period_number):
  ctx = callback_context
  input_id = ctx.triggered[0]["prop_id"].split(".")[0]
  if input_id == "time_period":
      planning_time = time_period_data[period_number]["planning_time"]
      start_yr = time_period_data[period_number]["start_yr"]

  if input_id in ["planning_time", "start_yr"]:
      period_number = None
  return planning_time, start_yr, period_number

@app.callback(
   Output("bar_chart", "figure"),
   Output("line_second", "figure"),
  Output("returns_chart", "figure"),
  Input("starting_amount", "value"),
  Input("planning_time", "value"),
  Input("start_years", "value"),
)
def update_totals(starting_amount,planning_time, start_years):
  starting_amount = 10 if starting_amount is None else starting_amount
  planning_time = 1 if planning_time is None else planning_time
  start_years = MIN_YEAR if start_years is None else int(start_years)

  max_time = MAX_YEAR + 1 - start_years
  planning_time = min(max_time, planning_time)
  if start_years + planning_time > MAX_YEAR:
      start_years = min(df.iloc[-planning_time, 0], MAX_YEAR)


  ds = backtest(planning_time, start_years)
  dc= backCap(planning_time, start_years)
  dt= backSec(planning_time, start_years)
  db = backBar(planning_time, start_years)

  fig = make_line_chart(ds)
  fig2=secondLine(dc, dt) if not dc.empty else thirdChart(dt)
  fig3=make_bar(db)

  return fig,fig2,fig3


if __name__ == "__main__":
  app.run(debug=True)