import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H1(children='Analiza branży informatycznej w Polsce'),

    html.Div(children='''
        W ramach projektu z zajęć z wizualizacji danych przygotowaliśmy graficzną analizę danych dotyczącą branży informatycznej oraz informatyków w Polsce.
        Jest ona podzielona na trzy części:
    '''),

    html.H3(children='1. Analiza ofert pracy dla informatyków'),

    html.Div(children='Tutaj wykorzystano dane z portalu PRACUJ.PL z lat 2018-2023'),

    html.H3(children='2. Analiza działalności zawodowej informatyków'),

    html.Div(children='''Wykorzystano tutaj dane z dwóch źródeł: STACK OVERFLOW, gdzie od 2011 r. programiści wypełniają ankiety dotyczące ich działalności, zatrudnienia i 
             umiejętności. Polacy uczestniczą w tych ankietach od 2014 r., jednak co roku rubryki w ankietach zmieniają się. Drugim źródłem danych jest GITHUB,
             gdzie znajdziemy statystyki na temat repozytoriów.'''),
])
