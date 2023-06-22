import dash
from dash import html
from app import pracuj_charts


dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children=''),
    
    
       html.Div(children=pracuj_charts.create_chart(), style={"min-height" : "450px"}),
        #html.H1(children='', style={"height": "450px"}),
        #html.Div(children=tree_chart_github.create_chart2())
        html.Div(children=pracuj_charts.create_chart2(), style={"min-height" : "450px"}),
     

   
    
])


