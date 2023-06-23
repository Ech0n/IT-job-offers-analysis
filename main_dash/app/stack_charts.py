import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

#data_source = "/content/drive/MyDrive/Wizualizacja danych/stack-overflow/"
data_source = "../data/stack-overflow/"

df2014 = pd.read_csv(data_source + "2014 Stack Overflow Survey Responses.csv")
df2015 = pd.read_csv(data_source + "2015 Stack Overflow Developer Survey Responses.csv", low_memory=False, skiprows=[0])
df2016 = pd.read_csv(data_source + "2016 Stack Overflow Survey Responses.csv")
df2017 = pd.read_csv(data_source + "survey_results_public_2017.csv")
df2018 = pd.read_csv(data_source + "survey_results_public_2018.csv", low_memory=False)
df2019 = pd.read_csv(data_source + "survey_results_public_2019.csv")
df2020 = pd.read_csv(data_source + "survey_results_public_2020.csv")
df2021 = pd.read_csv(data_source + "survey_results_public_2021.csv")
df2022 = pd.read_csv(data_source + "survey_results_public_2022.csv")

df2014 = df2014[df2014["What Country do you live in?"] == "Poland"]
df2015 = df2015[df2015["Country"] == "Poland"]
df2016 = df2016[df2016["country"] == "Poland"]
df2017 = df2017[df2017["Country"] == "Poland"]
df2018 = df2018[df2018["Country"] == "Poland"]
df2019 = df2019[df2019["Country"] == "Poland"]
df2020 = df2020[df2020["Country"] == "Poland"]
df2021 = df2021[df2021["Country"] == "Poland"]
df2022 = df2022[df2022["Country"] == "Poland"]

def languages(df, year, field_name, separator = ";", is_visible = False):
    langs = df[field_name].value_counts()
    ps = pd.Series(dtype = float)
    for ans in langs.index:
        langs = ans.split(separator)
        for l in langs:
            if l in ps.index:
              ps[l] = ps[l] + 1
            else:
              ps[l] = 1
    ps = ps.sort_values(ascending=False)
    return go.Bar(x=ps.index, y=ps.values, visible=is_visible)

def languages_through_years():
    fig = go.Figure(languages(df2016, 2016, "tech_do", separator = "; ", is_visible = True))
    fig.add_trace(languages(df2017, 2017, "HaveWorkedLanguage", separator = "; "))
    fig.add_trace(languages(df2018, 2018, "LanguageWorkedWith"))
    fig.add_trace(languages(df2019, 2019, "LanguageWorkedWith"))
    fig.add_trace(languages(df2020, 2020, "LanguageWorkedWith"))
    fig.add_trace(languages(df2021, 2021, "LanguageHaveWorkedWith"))
    fig.add_trace(languages(df2022, 2022, "LanguageHaveWorkedWith"))
    fig.update_layout(title = "Liczba osób, które pracowały w poszczególnych językach w 2016")
    
    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active=0,
            buttons=list(
                [dict(label = '2016',
                  method = 'update',
                  args = [{'visible': [True, False, False, False, False, False, False]},
                  {'title': "Liczba osób, które pracowały w poszczególnych językach w 2016"}]),
                 dict(label = '2017',
                  method = 'update',
                  args = [{'visible': [False, True, False, False, False, False, False]},
                  {'title': "Liczba osób, które pracowały w poszczególnych językach w 2017"}]),
                 dict(label = '2018',
                  method = 'update',
                  args = [{'visible': [False, False, True, False, False, False, False]},
                  {'title': "Liczba osób, które pracowały w poszczególnych językach w 2018"}]),
                 dict(label = '2019',
                  method = 'update',
                  args = [{'visible': [False, False, False, True, False, False, False]},
                  {'title': "Liczba osób, które pracowały w poszczególnych językach w 2019"}]),
                 dict(label = '2020',
                  method = 'update',
                  args = [{'visible': [False, False, False, False, True, False, False]},
                  {'title': "Liczba osób, które pracowały w poszczególnych językach w 2020"}]),
                 dict(label = '2021',
                  method = 'update',
                  args = [{'visible': [False, False, False, False, False, True, False]},
                  {'title': "Liczba osób, które pracowały w poszczególnych językach w 2021"}]),
                 dict(label = '2022',
                  method = 'update',
                  args = [{'visible': [False, False, False, False, False, False, True]},
                  {'title': "Liczba osób, które pracowały w poszczególnych językach w 2022"}]),
                ])
            )
        ])
    
    return fig
