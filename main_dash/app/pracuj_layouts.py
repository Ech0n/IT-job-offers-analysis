import pandas as pd
import os
from dash import html, dcc, callback, Output, Input, ctx
import plotly.express as px
import plotly.graph_objects as go
import os
import dash_daq as daq
from app import pracuj_charts

def create_chart():
    
    layout = [
        
        html.H1(children='Liczba wymaganych technologii w  ofertach pracy na pracuj.pl', style={'textAlign':'center'}),
        html.Div(children=dcc.Dropdown([str(i) for i in range(2023, 2020, -1)], '2023', id='dropdown-selection-pracuj-1', style={"color" : 'black','width':"50vw"}),style={"display":"flex","justify-content": "center"}),
        dcc.Graph(id='graph-content-pracuj-1'),
        daq.ToggleSwitch(
            id='my-toggle-switch-pracuj-1',
            value=False,
            color='black',
            label='Pokaż więcej',
            style={"color" : 'white', 'font-size' : '50%'},
            labelPosition='bottom',
        ),
        
    ]
    @callback(
        Output('graph-content-pracuj-1', 'figure'),
        [Input('my-toggle-switch-pracuj-1', 'value'),
        Input('dropdown-selection-pracuj-1', 'value')]
    )
    def update_graph(full, year):
        how_many_listed = 5
        if (full):
           how_many_listed = 100
        
        if year is None:
            year = '2023'
        
        return pracuj_charts.pracuj_exptected_chart(how_many_listed, full, year)
    
    return layout

def create_chart2():
    
    layout = [
        
        html.H1(children='Liczba opcjonalnych (nice to have) technologii w  ofertach pracy na pracuj.pl', style={'textAlign':'center'}),
        html.Div(children=dcc.Dropdown([str(i) for i in range(2023, 2020, -1)], '2023', id='dropdown-selection-pracuj-2', style={"color" : 'black','width':"50vw"}),style={"display":"flex","justify-content": "center"}),
        
        # dcc.Dropdown([str(i) for i in range(2023, 2020, -1)], '2023', id='dropdown-selection-pracuj-2', style={"color" : 'black','width':"50vw"}),
        dcc.Graph(id='graph-content-pracuj-2'),
        daq.ToggleSwitch(
            id='my-toggle-switch-pracuj-2',
            value=False,
            color='black',
            label='Pokaż więcej',
            style={"color" : 'white', 'font-size' : '50%'},
            labelPosition='bottom',
            
        ),
    ]

    @callback(
        Output('graph-content-pracuj-2', 'figure'),
        [Input('my-toggle-switch-pracuj-2', 'value'),
        Input('dropdown-selection-pracuj-2', 'value')]
    )
    def update_graph(full, year):
        how_many_listed = 5
        if (full):
           how_many_listed = 100
        
        if year is None:
            year = '2023'
        return pracuj_charts.pracuj_optional_chart(how_many_listed, full, year)
    
    return layout

def benefits_dynamic():
    layout = [
        html.H1(children='Czy pracodawcy wymagają wykształcenia wyższego?', style={'textAlign':'center'}),
        dcc.RadioItems([10, 25,50], 10,id="benefits-radio"),
        dcc.Graph(id='graph-benefits-dif'), 
    ]

    @callback(
        Output('graph-benefits-dif', 'figure'),
        [Input('benefits-radio','value')]
    )
    def update_graph(count):
        return go.Figure(pracuj_charts.benefits(count))
    
    return layout

create_chart_driving_license  = [
        html.H1(children='Czy pracodawcy wymagają wykształcenia wyższego?', style={'textAlign':'center'}),        
        dcc.Graph(id='graph-content-pracuj-4',figure=pracuj_charts.chart_is_driving_license_required()),
    ]

create_chart_degree  = [
        html.H1(children='Czy pracodawcy wymagają wykształcenia wyższego?', style={'textAlign':'center'}),
        dcc.Graph(id='graph-content-pracuj-3',figure=pracuj_charts.chart_is_degree_required()),
    ]

liczba_ofert = [
#        html.H1(children='Czy pracodawcy wymagają wykształcenia wyższego?', style={'textAlign':'center'}),
        dcc.Graph(id='graph-content-pracuj-5',figure=pracuj_charts.chart_number_of_offers()),
    ]

types_of_contract = [
#        html.H1(children='Czy pracodawcy wymagają wykształcenia wyższego?', style={'textAlign':'center'}),
        dcc.Graph(id='graph-content-pracuj-5',figure=pracuj_charts.chart_types_of_contract()),
    ]

experience_level = [
        # html.H1(children='Stanowisko', style={'textAlign':'center'}),
        dcc.Graph(id='graph-content-pracuj-5',figure=pracuj_charts.chart_experience_level()),
    ]

# benefits = [
#         html.H1(children='Czy pracodawcy wymagają wykształcenia wyższego?', style={'textAlign':'center'}),
#         dcc.Graph(id='graph-content-pracuj-5',figure=pracuj_charts.benefits(10)),
#     ]

diffrent_benefits = [
        html.H1(children='Jakie benefity oferują pracodawcy', style={'textAlign':'center'}),
        dcc.Graph(id='graph-content-pracuj-5',figure=pracuj_charts.different_benefits()),
    ]

salaries = [
        html.H1(children='Zarobki programistów:', style={'textAlign':'center'}),
        dcc.Graph(id='graph-content-pracuj-5',figure=pracuj_charts.salaries()),
    ]

other_requirements = [
        html.H1(children='Wymagania pracodawców:', style={'textAlign':'center'}),
        dcc.Graph(id='graph-content-pracuj-5',figure=pracuj_charts.other_requirements()),
    ]

salary_by_region = [
        html.H1(children='Zarobki programistów według województwa:', style={'textAlign':'center'}),
        dcc.Graph(id='graph-content-pracuj-5',figure=pracuj_charts.salary_by_region()),
    ]

salary_trend = [
        html.H1(children='Zarobki programistów na przestrzeni czasu:', style={'textAlign':'center'}),
        dcc.Graph(id='graph-content-pracuj-5',figure=pracuj_charts.salaries_trend()),
    ]

requirements = [
        html.H1(children='Trend technologi deklarowanych jako wymagane przez pracodawców:', style={'textAlign':'center'}),
        dcc.Graph(id='graph-content-pracuj-5',figure=pracuj_charts.requirements()),
    ]

offers_by_region = [
        html.H1(children='Liczba ofert pracy w poszczególnych województwach:', style={'textAlign':'center'}),
        dcc.Graph(id='graph-content-pracuj-5',figure=pracuj_charts.offers_by_region(),style={'width': '80vh', 'height': '80vh', 
       }),
    ]


# offers_by_region = [
#     html.H1(children='Zarobki programistów:', style={'textAlign':'center'}),
#     dcc.Graph(id='graph-content-pracuj-5',figure=pracuj_charts.location()),
# ]