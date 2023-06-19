from dash import Dash, html, dcc
import dash
import app.components.navbar as nv
import dash_bootstrap_components as dbc



app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.QUARTZ])

app.layout = html.Div([

    html.Div([nv.navbar]),
    html.H1('Multi-page app with Dash Pages'),

	dash.page_container
])


#app.layout = html.Div(children=[html.Div(charts.create_chart())
                      #,html.Div(bubble_chart.create_chart())])
#bubble_chart.create_chart()
