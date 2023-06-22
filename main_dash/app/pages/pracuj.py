import dash
from dash import html, dcc, callback, Output, Input
from app import pracuj_charts
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children=''),
    
    
       html.Div(children=pracuj_charts.create_chart(), style={"min-height" : "1200px"}),
        #html.H1(children='', style={"height": "450px"}),
        #html.Div(children=tree_chart_github.create_chart2())
     

   
    
])


