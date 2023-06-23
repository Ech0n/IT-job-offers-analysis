import dash
from dash import html
from app import pracuj_layouts
import dash_bootstrap_components as dbc


dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children=''),
    
    
       html.Div(children=pracuj_layouts.create_chart(), style={"min-height" : "450px"}),
        #html.H1(children='', style={"height": "450px"}),
        #html.Div(children=tree_chart_github.create_chart2())
        html.Hr(),
        html.Div(children=pracuj_layouts.create_chart2(), style={"min-height" : "450px"}),
        # dbc.Row([
        #     html.Div(children=pracuj_layouts.create_chart_driving_license, style={"min-height" : "450px",'width':"50%"}),
        # ]),
        html.Hr(),
        html.Div(children=pracuj_layouts.liczba_ofert, style={"min-height" : "550px"}),
        html.Hr(),
        html.Div(children=pracuj_layouts.offers_by_region, style={"min-height" : "650px","width":"100%",
        'display':'flex',
        'flex-direction':'column',
        'justify-content':'center',
        'align-items' : 'center'}),
        html.Hr(),
        html.Div(children=pracuj_layouts.types_of_contract, style={"min-height" : "450px"}),
        html.Hr(),
        html.Div(children=pracuj_layouts.experience_level, style={"min-height" : "450px"}),
        html.Hr(),
        # html.Div(children=pracuj_layouts.benefits_dynamic(), style={"min-height" : "450px"}),
        html.Div(children=pracuj_layouts.diffrent_benefits, style={"min-height" : "450px"}),
        html.Hr(),
        html.Div(children=pracuj_layouts.salaries, style={"min-height" : "450px"}),
        html.Hr(),
        html.Div(children=pracuj_layouts.salary_by_region, style={"min-height" : "650px"}),
        html.Hr(),
        html.Div(children=pracuj_layouts.salary_trend, style={"min-height" : "450px"}),
        html.Hr(),
        # html.Div(children=pracuj_layouts.offers_by_region, style={"min-height" : "450px"}),
        html.Div(children=pracuj_layouts.create_chart_degree, style={"min-height" : "450px",'width':"100%"}),
        html.Hr(),
        html.Div(children=pracuj_layouts.other_requirements, style={"min-height" : "450px"}),
        html.Hr(),
        html.Div(children=pracuj_layouts.requirements, style={"min-height" : "800px"}),
])


