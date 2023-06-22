import pandas as pd
import os
from dash import html, dcc, callback, Output, Input, ctx
import plotly.express as px
import plotly.graph_objects as go
import os
import dash_daq as daq
from app import stack_charts


# languages_through_years = [
#         html.H1(children='Zarobki programistów:', style={'textAlign':'center'}),
#         dcc.Graph(id='graph-content-pracuj-5',figure=stack_charts.languages_through_years()),
#     ]