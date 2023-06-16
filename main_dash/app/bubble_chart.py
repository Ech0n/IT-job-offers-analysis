import plotly.graph_objects as go
import pandas as pd
from app import app
from dash import html, dcc, callback, Output, Input

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

    df = pd.read_csv('assets\github_data29_05_2023_with_category.csv')
    layout = [
        html.H1(children='Title of Dash App2', style={'textAlign':'center'}),
        dcc.Dropdown(df.category.unique(), 'programming', id='dropdown-selection2'),
        dcc.Graph(id='graph-content2', responsive=True)
    ]
    

    @callback(
        Output('graph-content2', 'figure'),
        Input('dropdown-selection2', 'value')
    )
    def update_graph(value):
        dff = df[df.category==value]
        return github_bubble_chart(dff)
    return layout
    
def github_bubble_chart(df):

    df = df.sort_values('total_num_of_repos', ascending=False)
   
    x, y = distribute_xy(0, 150000, 5000, -22000, len(df))
    
    def prepare_colors(desc):
        
        colors = []
        for d in desc:
            for key in colors_dict.keys():
                if key.lower() in d.lower():
                    colors.append(colors_dict[key])
                    
                    break
        return colors
            



    #fig = px.scatter(x=x, y=y,
	         #size=df['total_num_of_repos'],
               #  hover_name=df['desc'],
               #  labels={"x" : " ", "y" : " "},
               #  )
    size = df['total_num_of_repos']
    colors = prepare_colors(df['desc'])

    fig = go.Figure(data=[go.Scatter(
    x=x,
    y=y,
    text=df['title'],
    mode='markers+text',
    textposition='bottom center',

    hovertext = df['desc'],
    hoverinfo = 'text',

    marker=dict(
        size=size,
        sizemode='area',
        sizeref=2.*max(size)/(360.**2),
        sizemin=10,
        color = colors,
        
    )
)
])
    fig.update_layout( showlegend=False, autosize=True)

    import plotly.express as px

    fig = px.treemap(df, path=[px.Constant("all"), 'category', 'title'], values='total_num_of_repos', hover_name='desc'
                     )
    fig.update_traces(root_color="lightgrey")
    #fig.update_traces(hovertemplate='num%{desc}<br>total number of repos=%{value}<extra></extra>')
    fig.update_traces(hovertemplate='<b>%{hovertext}</b><br><br><br>Total number of repos : %{value}<extra></extra>')
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
    
    #graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return fig

def distribute_xy(start_x, start_y, x_step, y_step, numPoints, max_X=15000):
    x = []
    y = []
    x_copy = start_x
    for i in range(numPoints):
        x.append(start_x)
        y.append(start_y)
        start_x += x_step
        if (start_x > max_X):
            start_x = x_copy
            start_y += y_step
            x_step = x_step * 0.98
            y_step = y_step * 0.95
    return x, y