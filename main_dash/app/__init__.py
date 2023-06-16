from dash import Dash, html

app = Dash(__name__)

from app import charts, bubble_chart

app.layout = html.Div(children=[html.Div(charts.create_chart())
                      ,html.Div(bubble_chart.create_chart())])
#bubble_chart.create_chart()
