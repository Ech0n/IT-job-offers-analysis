import plotly.graph_objects as go
import pandas as pd
from dash import html, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

import os
import dash_daq as daq


colors_dict = {
            'programming' : '#2F3C7E',
            'SQL' : '#99F443',
            'framework' : '#FEE715',
            'database' : '#CCF381',
            'game' : '#00FFFF',
            'open source': 'green',
            'operating system' : 'blue',
            'automation' : '#CBD18F',
            'command-line' : 'yellow',
            'learning' : 'purple',
            'control' : '#FFA351',
            'cloud' : '#8A307F',
            'web' : '#201E20',
            'language': '#1E2761',
            'graphics' : 'pink',
            '' : 'red'
        }

def create_chart():

    df = pd.read_csv(os.path.join('app', 'assets','github_data29_05_2023_with_category.csv')
)
    layout = [
        html.H1(children='Popularnosc technologii wedlug liczby repozytoriow na githubie:', style={'textAlign':'center'}),
        
        # dcc.Dropdown(list(df.category.unique()) + ['all'], 'all', id='dropdown-selection2', style={"display":"flex","color" : 'black','width':"50vw","justify-content":"center"}),

        dbc.Row([
            
            html.Div(children=dcc.Dropdown(list(df.category.unique()) + ['all'], 'all', id='dropdown-selection2',style={"display":"block","width":"200px"}), style={"display":"flex","color" : 'black','width':"200px","justify-content":"center"}),
            html.Div(children="Koloruj po absolutniej populatności: ",style={"margin-left":"50px","width":"300px"}),
            daq.ToggleSwitch(
                id='my-toggle-switch',
                value=False,
                color='black',
                style={"width":"10%"}
            ),
        ],justify="center"),
        
        dcc.Graph(id='graph-content2', responsive=True)
    ]
    

    @callback(
        Output('graph-content2', 'figure'),
        [Input('dropdown-selection2', 'value'),
        Input('my-toggle-switch', 'value' )]
    )
    
    def update_graph(value, value2):
        dff = None
        
        if value == 'all':
            dff = df
            
        else:
            dff =  df[df.category==value]
            

        return github_tree_chart(dff, 'total_num_of_repos', value2)
    return layout

def create_chart2():
    df = pd.read_csv(os.path.join('app', 'assets','github_data29_05_2023_with_category.csv')
    )
    layout = [
        html.H1(children='Popularnosc technologii wedlug TOP 1 repozytorium(liczby gwiazdek) na githubie:', style={'textAlign':'center'}),

        dbc.Row([
            
            html.Div(children=dcc.Dropdown(list(df.category.unique()) + ['all'], 'all', id='dropdown-selection3',style={"display":"block","width":"200px"}), style={"display":"flex","color" : 'black','width':"200px","justify-content":"center"}),
            html.Div(children="Koloruj po absolutniej populatności: ",style={"margin-left":"50px","width":"300px"}),
            daq.ToggleSwitch(
                id='my-toggle-switch2',
                value=False,
                color='black',
                style={"width":"10%"}
            ),
        ],justify="center"),
        
        dcc.Graph(id='graph-content3', responsive=True)
    ]
    

    @callback(
        Output('graph-content3', 'figure'),
        [Input('dropdown-selection3', 'value'),
         Input('my-toggle-switch2', 'value')]
        
    )
    def update_graph(value, color_scale):
        dff = None
        
        if value == 'all' or value is None:
            dff = df
            
        else:
            dff =  df[df.category==value]
            

        return github_tree_chart(dff, 'stars', color_scale)
    return layout

def github_tree_chart(df, sort_by, color_scale):

    df = df.sort_values(sort_by, ascending=False)
   
    #x, y = distribute_xy(0, 150000, 5000, -22000, len(df))
    
    # def prepare_colors(desc):
        
    #     colors = []
    #     for d in desc:
    #         for key in colors_dict.keys():
    #             if key.lower() in d.lower():
    #                 colors.append(colors_dict[key])
                    
    #                 break
    #     return colors
            



    #fig = px.scatter(x=x, y=y,
	         #size=df[sort_by],
               #  hover_name=df['desc'],
               #  labels={"x" : " ", "y" : " "},
               #  )
#     size = df[sort_by]
#     colors = prepare_colors(df['desc'])

#     fig = go.Figure(data=[go.Scatter(
#     x=x,
#     y=y,
#     text=df['title'],
#     mode='markers+text',
#     textposition='bottom center',

#     hovertext = df['desc'],
#     hoverinfo = 'text',

#     marker=dict(
#         size=size,
#         sizemode='area',
#         sizeref=2.*max(size)/(360.**2),
#         sizemin=10,
#         color = colors,
        
#     )
# )
# ])
    #fig.update_layout( showlegend=False, autosize=True)
    fig = None
    if (color_scale):
        fig = px.treemap(df, path=[px.Constant("all"), 'category', 'title'], values=sort_by, hover_name='desc',
                        color=sort_by
                     )
    elif color_scale is False: fig = px.treemap(df, path=[px.Constant("all"), 'category', 'title'], values=sort_by, hover_name='desc',
                        
                     )
    
    fig.update_traces(root_color="lightgrey")
    #fig.update_traces(hovertemplate='num%{desc}<br>total number of repos=%{value}<extra></extra>')
    fig.update_traces(hovertemplate='<b>%{label}</b><br><br><b>%{hovertext}</b><br><br><br>Number : %{value}<extra></extra>')
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    
    #x axis
    fig.update_xaxes(visible=False)

    #y axis    
    fig.update_yaxes(visible=False)

    fig.update_layout(
    font=dict(
        family="Courier New, monospace",
        size=18,  # Set the font size here
        color="black",
    )
    )
    fig.update_layout( # make transparent background
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family="Courier New",
        font_color="white",
    ) 
    
    
    #graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return fig

# def distribute_xy(start_x, start_y, x_step, y_step, numPoints, max_X=15000):
#     x = []
#     y = []
#     x_copy = start_x
#     for i in range(numPoints):
#         x.append(start_x)
#         y.append(start_y)
#         start_x += x_step
#         if (start_x > max_X):
#             start_x = x_copy
#             start_y += y_step
#             x_step = x_step * 0.98
#             y_step = y_step * 0.95
#     return x, y