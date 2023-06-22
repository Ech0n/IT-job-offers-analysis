import pandas as pd
import os

from dash import html, dcc, callback, Output, Input, ctx
import plotly.express as px

import os
import dash_daq as daq



def create_chart():
    
    layout = [
        
        html.H1(children='Technologie w wymaganiach ofert pracy pracuj.pl:', style={'textAlign':'center'}),
        
        dcc.Graph(id='graph-content-pracuj-1'),
        dcc.Dropdown([str(i) for i in range(2023, 2019, -1)], '2023', id='dropdown-selection-pracuj-1', style={"color" : 'black'}),
        daq.ToggleSwitch(
            id='my-toggle-switch-pracuj-1',
            value=False,
            color='black',
            label='Pokaz wiecej',
            style={"color" : 'black', 'font-size' : '50%'},
            labelPosition='bottom',
            
        ),
        daq.BooleanSwitch(id='my-boolean-switch-pracuj1', on=False),
        
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
        


           
        return pracuj_exptected_chart(how_many_listed, full, year)
    
    return layout

def pracuj_exptected_chart(how_many_listed, full, year):
    file_columns = open(os.path.join('app', 'assets','kolumny_pracuj(2).txt'), "r", encoding="utf-8")
    columns_list = []
    for line in file_columns:
        columns_list = line.split()
    file_columns.close()
   

    columns_expected = []
    for column in columns_list:
      if 'wymagane' in column:
        columns_expected.append(column)

    pracuj = pd.read_csv(os.path.join('app', 'assets','pracuj(2).csv'), encoding="utf-8", dtype=str, delimiter=";", names=columns_list, header=None, low_memory=False, usecols=columns_expected+['rok'])
    pracuj = pracuj[pracuj['rok'] == year]
    
    df = pd.DataFrame(columns=['Name', 'Number'])
    
    for i, column in enumerate(columns_expected):
       number = pracuj[column].value_counts()
       if ('1' not in number):
          number['1'] = 0
       df.loc[i] = [column.removeprefix('wymagane-'),number['1']]

  
    
    df = df.sort_values('Number', ascending=False)
    
    fig = None
    if full:
           fig = px.bar(df.iloc[:how_many_listed], x='Number', y='Name', orientation='h', height=4000, color='Name')
    else:
        fig = px.bar(df.iloc[:how_many_listed], x='Number', y='Name', orientation='h',height=450,  color='Name')


    fig.update_layout( # make transparent background
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    ) 
    fig.update_layout(
    font=dict(
        family="Courier New, monospace",
        size=18,  # Set the font size here
        color="black",
    )
        )
    return fig
      