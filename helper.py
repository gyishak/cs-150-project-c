from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px


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
Helper Funtion
"""
def backCap(nper, start_yr):
   end_yr = start_yr + nper - 1
   dc = electric[(electric["Year"] >= start_yr) & (electric["Year"] <= end_yr)]
   return dc


def backBar(nper, start_yr):
   end_yr = start_yr + nper - 1
   ds = df[(df["Year"] >= start_yr) & (df["Year"] <= end_yr)]
   return ds


def backtest(nper, start_yr):
  end_yr = start_yr + nper - 1
  ds=dataHouse[(dataHouse["Year"]>=start_yr) & (dataHouse["Year"]<=end_yr)]
  return ds


def backSec(nper, start_yr):
  end_yr = start_yr + nper - 1
  ds=dataTransp[(dataTransp["Year"]>=start_yr) & (dataTransp["Year"]<=end_yr)]
  return ds


"""
===========================================================================
Chart
"""
def make_bar(df):
   start = df .iloc[0]["Year"]
   yrs = len(df)
   fig = go.Figure(
       data=[
           go.Bar(
               x=df["Year"],
               y=df["Income"],
               textposition="inside",
               hoverinfo="x+y",
           )
       ]
   )
   fig.update_layout(
       title=f"Income Spanning {yrs} Years",
       template="none",
       yaxis=dict(tickprefix="$", fixedrange=True),
       xaxis=dict(title="Year", fixedrange=True)
    )
   return fig

def make_line_chart(dataHouse):
   start=dataHouse.iloc[0]["Year"]
   yrs=len(dataHouse)
   dtick= 1 if yrs<16 else 2 if 16<=yrs<30  else 5

   fig=go.Figure()
   fig.add_trace(
      go.Scatter(
          x=dataHouse["Year"].tolist(),
          y=dataHouse["Price"].tolist(),
          name="House Prices",
          marker_color="#008000"
      )
   )
   fig.update_layout(
      title=f"House Prices Spanning {yrs} Years",
      template="none",
      showlegend=True,
      legend=dict(x=0.01, y=0.99),
      height=400,
      margin=dict(l=40, r=10, t=60, b=55),
      yaxis=dict(tickprefix="$", fixedrange=True),
      xaxis=dict(title="Year", fixedrange=True, dtick=dtick), )
   return fig

def thirdChart(dataTransp):
    #start = dataTransp.iloc[0]["Year"]
    yrs = len(dataTransp)
    dtick = 1 if yrs < 16 else 2 if 16 <= yrs < 30 else 5

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dataTransp["Year"].tolist(),
            y=dataTransp["Price"].tolist(),
            name="House Prices",
            marker_color="#FFA500"
        )
    )
    fig.update_layout(
      title=f"House Prices Spanning {yrs} Years",
      template="none",
      showlegend=True,
      legend=dict(x=0.01, y=0.99),
      height=400,
      margin=dict(l=40, r=10, t=60, b=55),
      yaxis=dict(tickprefix="$", fixedrange=True),
      xaxis=dict(title="Year", fixedrange=True, dtick=dtick), )
    return fig

def secondLine(electric, dataTransp):
   start = dataTransp.iloc[0]["Year"]
   yrs = len(dataTransp)
   dtick = 1 if yrs < 16 else 2 if 16 <= yrs < 30 else 5


   fig=go.Figure()
   fig.add_trace(
      go.Scatter(
          x=electric["Year"].tolist(),
          y=electric["Price"].tolist(),
          name="Electricity Expenses",
          marker_color="#964B00"
      )
   )
   fig.add_trace(
       go.Scatter(
           x=dataTransp["Year"].tolist(),
           y=dataTransp["Price"].tolist(),
           name="Gasoline Prices",
           marker_color="#FFA500"
       )
   )
   fig.update_layout(
      title=f"Gasoline Prices and Electricity Expenses Spanning {yrs} Years",
      template="none",
      showlegend=True,
      legend=dict(x=0.01, y=0.99),
      height=400,
      margin=dict(l=40, r=10, t=60, b=55),
      yaxis=dict(tickprefix="$", fixedrange=True),
      xaxis=dict(title="Year", fixedrange=True, dtick=dtick),
   )
   return fig

"""
===========================================================================
Tables
"""
house_price_table=dash_table.DataTable(
   id="house_price_tabl",
   columns=[
               {"name": "Year", "id": "Year"},
               {"name": "Home Price ($)", "id": "Price"}
           ],
   data=data1,
   page_size=15,
   style_table={"overflowX": "scroll"}
)
income_table=dash_table.DataTable(
   id="income_tabl",
   columns=[
               {"name": "Year", "id": "Year"},
               {"name": "Income ($)", "id": "Income"}
           ],
   data=data2,
   page_size=15,
   style_table={"overflowX": "scroll"}
)


trans_table=dash_table.DataTable(
   id="transp_table",
   columns=[
               {"name": "Year", "id": "Year"},
               {"name": "Gasoline Price ($ per gallon)", "id": "Price"}
           ],
   data=data3,
   page_size=15,
   style_table={"overflowX": "scroll"}
)
ele_table=dash_table.DataTable(
   id="ele_table",
   columns=[
               {"name": "Year", "id": "Year"},
               {"name": "Electricity Price ($ per kWh) ", "id": "Price"}
           ],
   data=data4,
   page_size=15,
   style_table={"overflowX": "scroll"}
)


