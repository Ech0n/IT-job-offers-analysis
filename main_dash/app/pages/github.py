import dash
from dash import html, dcc, callback, Output, Input
from app import tree_chart_github
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children=''),
    
    
       html.Div(children=tree_chart_github.create_chart(), style={"min-height" : "600px"}),
        #html.H1(children='', style={"height": "450px"}),
        html.Hr(),
        html.Div(children=tree_chart_github.create_chart2())
     

   
    
])


