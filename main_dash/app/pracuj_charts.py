import pandas as pd
import os

from dash import html, dcc, callback, Output, Input, ctx
import plotly.express as px
import plotly.graph_objects as go
import warnings
import os
import geojson
import dash_daq as daq

#### ŁADUJEMY DANE
with open("./app/assets/poland.geojson","r",encoding="utf-8") as f:
    polmap = geojson.load(f)

file_columns = open(os.path.join('app', 'assets',"kolumny_pracuj(3).txt"), "r", encoding="utf-8")
columns_list = []
for line in file_columns:
    columns_list = line.split()
file_columns.close()

pracuj = pd.read_csv("./app/assets/pracuj(5).csv",names=columns_list,delimiter=";", encoding="utf-8", dtype=str)

def load_data(filename_columns, filename_main, column_prefix):
    file_columns = open(os.path.join('app', 'assets',filename_columns), "r", encoding="utf-8")
    columns_list = []
    for line in file_columns:
        columns_list = line.split()
    file_columns.close()
   

    columns_expected = []
    for column in columns_list:
      if column_prefix in column:
        columns_expected.append(column)

    # pracuj = pd.read_csv(os.path.join('app', 'assets',filename_main), encoding="utf-8", dtype=str, delimiter=";", names=columns_list, header=None, low_memory=False, usecols=columns_expected+['rok'])
    # pracuj = pd.read_csv("./app/assets/"+filename_main,names=columns_list,delimiter=";",dtype=str)
    years = pracuj.rok.unique()
    
    df = pd.DataFrame(columns=['Name', 'Number'])
    all_df = {}
    for year in years:
        pracuj_year = pracuj[pracuj['rok'] == year]
        
        for i, column in enumerate(columns_expected):
            
            number = pracuj_year[column].value_counts()

            if ('1' not in number):
                number['1'] = 0
            df.loc[i] = [column.removeprefix(column_prefix),number['1']]

        df = df.sort_values('Number', ascending=False)
        all_df[year] = df
        df = pd.DataFrame(columns=['Name', 'Number'])
    
    
    return all_df


### PRZETWARZANIE DANYCH
with warnings.catch_warnings():
  requirements = {}
  pracuj2 = pracuj[pracuj["rok"] > "2020"]
  for c in pracuj2.columns:
    if c.startswith("wymagane-"):
      requirements[c] = []
      pracuj3 = pracuj2[pracuj2["rok"] == "2021"]
      for m in range(1, 13):
        pracuj4 = pracuj3[pracuj3["month"] == m]
        number_of_requirements = 0
        for _, p in pracuj4.iterrows():
          if p[c] == "1":
            number_of_requirements += 1
        '''pracuj5 = pracuj4[pracuj4[c == "1"]]
        number_of_requirements = len(pracuj5)'''
        requirements[c].append(number_of_requirements)
      pracuj3 = pracuj2[pracuj2["rok"] == "2022"]
      for m in range(1, 13):
        pracuj4 = pracuj3[pracuj3["month"] == m]
        number_of_requirements = 0
        for _, p in pracuj4.iterrows():
          if p[c] == "1":
            number_of_requirements += 1
        '''pracuj5 = pracuj4[pracuj4[c == "1"]]
        number_of_requirements = len(pracuj5)'''
        requirements[c].append(number_of_requirements)
      pracuj3 = pracuj2[pracuj2["rok"] == "2023"]
      for m in range(1, 6):
        pracuj4 = pracuj3[pracuj3["month"] == m]
        number_of_requirements = 0
        for _, p in pracuj4.iterrows():
          if p[c] == "1":
            number_of_requirements += 1
        '''pracuj5 = pracuj4[pracuj4[c == "1"]]
        number_of_requirements = len(pracuj5)'''
        requirements[c].append(number_of_requirements)

all_df_exptected = load_data("kolumny_pracuj(3).txt","pracuj(5).csv", 'wymagane-')
all_df_optional = load_data("kolumny_pracuj(3).txt","pracuj(5).csv", 'opcjonalne-')
offer_count = 0
wykształcenie_count = 0
prawko_count = 0
required_count = 0
experience_count = 0
dosiwadczenie = {}
team_sizes = set()
for i , r in pracuj.iterrows():
    offer_count += 1
    l = r["wykształcenie-wyższe"]
    if l != '-1':
        required_count += 1
    if l == '1':
        wykształcenie_count+=1
    if r["prawo-jazdy"] == '1':
        prawko_count+=1
    if r["experience"]!='-1':
        experience_count+=1
        if(r["experience"] not in dosiwadczenie):
            dosiwadczenie[r["experience"]] = 0
        dosiwadczenie[r["experience"]] +=1

    team_size = r["rozmiar-zespolu"]
    team_sizes.add(team_size)



#### TWORZENIE WYKRESOW
def chart_is_degree_required():
    values = [wykształcenie_count,required_count-wykształcenie_count]
    labels = ["Oferty wymagające wykształcenia wyższego","Oferty nie wymagające wykształcenia wyższego"]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    return fig


def chart_is_driving_license_required():
    values = [prawko_count,required_count-prawko_count]
    labels = ["Oferty wymagające prawa jazdy","Oferty nie wymagające prawa jazdy"]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    return fig


def pracuj_exptected_chart(how_many_listed, full, year):
    
    fig = None
    if full:
           fig = px.bar(all_df_exptected[year].iloc[:how_many_listed], x='Number', y='Name', orientation='h', height=4000, color='Name')
    else:
        fig = px.bar(all_df_exptected[year].iloc[:how_many_listed], x='Number', y='Name', orientation='h',height=450,  color='Name')


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

def pracuj_optional_chart(how_many_listed, full, year):
    
    fig = None
    if full:
           fig = px.bar(all_df_optional[year].iloc[:how_many_listed], x='Number', y='Name', orientation='h', height=4000, color='Name')
    else:
        fig = px.bar(all_df_optional[year].iloc[:how_many_listed], x='Number', y='Name', orientation='h',height=450,  color='Name')


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


def chart_number_of_offers():
  pracuj["month"] = pd.to_numeric(pracuj["month"])
  groupped = pracuj.groupby(["rok", "month"])
  counts = groupped["company"].count()
  counts = counts.sort_index(level=["rok", "month"], ascending=[True, True])
  data_list = counts.tolist()

  for i in range(12 - len(counts[counts.index.get_level_values("rok").unique()[0]])):
    data_list.insert(0, 0)
  for i in range(12 - len(counts[counts.index.get_level_values("rok").unique()[-1]])):
    data_list.append(0)
  data_matrix = []
  for i in range(0, len(data_list), 12):
    data_matrix.append(data_list[i:i+12])

  fig = px.imshow(data_matrix,
                  title="Liczba ofert w poszczególnych latach i miesiącach",
                  labels=dict(x="Miesiąc", y="Rok", color="Liczba ofert"),
                  x=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
                  y=counts.index.get_level_values("rok").unique(),
                  color_continuous_scale="Blues"
                  )
  return fig


def chart_types_of_contract():
  types = ["umowa-o-prace", "b2b", "umowa-zlecenie", "umowa-o-dzieło", "umowa-o-staż", "umowa-agencyjna", "umowa-na-zastępstwo"]
  names = ["Umowa o pracę", "B2B", "Umowa zlecenie", "Umowa o dzieło", "Umowa o staż", "Umowa agencyjna", "Umowa na zastępstwo"]
  number_of_offers = []
  for t in types:
    pracuj[t] = pd.to_numeric(pracuj[t])
    number = 0
    for i in range(len(pracuj[t])):
      if pracuj[t][i] == 1:
        number += 1
    number_of_offers.append(number)
  
  fig = dict({
    "data": [{"type": "bar",
              "x": names,
              "y": number_of_offers}],
    "layout": {"title": {"text": "Liczba ofert pracy z określonymi formami umów"}}
  })
  
#   pio.show(fig)
  return fig

def chart_experience_level():
  level = ["-1", "intern", "junior", "mid", "senior"]
  d = dict()
  for l in level:
    d[l] = 0
  for i in range(len(pracuj["experience-level"])):
    d[pracuj["experience-level"][i]] += 1
  d.pop("-1")
  k = list(d.keys())
  v = list(d.values())
  
  fig = px.pie(values=v, names=k, title="Liczba osób na poszczególnych stanowiskach")
  return fig


def benefits(number_of_benefits, is_visible=False, show_all = False):
    benefits = {}

    for c in pracuj.columns:
        if c.startswith("benefit-"):
            groupped = pracuj.groupby(c)
            values = groupped["company"].count()
            benefits[c] = [values[2]]
    
    df = pd.DataFrame(benefits).T
    df.columns = ["Oferowany"]
    df = df.sort_values("Oferowany", ascending=False)
    if show_all == False:
        df = df.head(number_of_benefits)
    df = df.sort_values("Oferowany")
    #   fig = go.Bar(y=df.index, x=df["Oferowany"])
    fig = go.Bar(y=df.index, x=df["Oferowany"], visible=is_visible, orientation="h")
    return fig


def different_benefits():
  fig = go.Figure(benefits(10, is_visible=True))
  fig.add_trace(benefits(15))
  fig.add_trace(benefits(20))
  fig.add_trace(benefits(25))
  fig.add_trace(benefits(30))
  fig.add_trace(benefits(10, show_all=True))
  fig.update_layout(title = "10 najczęściej oferowanych benefitów")

  fig.update_layout(
      updatemenus=[go.layout.Updatemenu(
          active=0,
          direction="down",
          buttons=list(
              [dict(label = "10",
                    method ="update",
                    args = [{"visible" : [True, False, False, False, False, False]},
                            {"title" : "10 najczęściej oferowanych benefitów"}]),
               dict(label = "15",
                    method ="update",
                    args = [{"visible" : [False, True, False, False, False, False]},
                            {"title" : "15 najczęściej oferowanych benefitów"}]),
               dict(label = "20",
                    method ="update",
                    args = [{"visible" : [False, False, True, False, False, False]},
                            {"title" : "20 najczęściej oferowanych benefitów"}]),
              dict(label = "25",
                    method ="update",
                    args = [{"visible" : [False, False, False, True, False, False]},
                            {"title" : "25 najczęściej oferowanych benefitów"}]),
               dict(label = "30",
                    method ="update",
                    args = [{"visible" : [False, False, False, False, True, False]},
                            {"title" : "30 najczęściej oferowanych benefitów"}]),
               dict(label = "Pokaż wszystkie",
                    method ="update",
                    args = [{"visible" : [False, False, False, False, False, True]},
                            {"title" : "Wszystkie benefity oferowane przez pracodawcę"}])
               ],
          ),
          x=1,
          y=1.1
      )]
  )
  
  fig.update_layout(margin=dict(l=20, r=20, t=60, b=20), height=700)
  return fig


def salaries():
  locations = ["mazowieckie", "dolnośląskie", "małopolskie", "śląskie", "łódzkie", "wielkopolskie", "opolskie", "podlaskie", "zachodnio-pomorskie", "podkarpackie", "lubelskie", "lubuskie", "świętokrzyskie", "warmińsko-mazurskie", "kujawsko-pomorskie", "pomorskie"]
  salaries = []
  pracuj["salary"] = pd.to_numeric(pracuj["salary"])
  for l in locations:
    pracuj[l] = pd.to_numeric(pracuj[l])
    salaries_sum = 0
    number = 0
    for i in range(len(pracuj[l])):
      if pracuj[l][i] == 1 and pracuj["salary"][i] != -1:
        number += 1
        salaries_sum += pracuj["salary"][i]
    salaries.append(salaries_sum/number)
  
  fig = dict({
    "data": [{"type": "bar",
              "x": locations,
              "y": salaries}],
    "layout": {"title": {"text": "Średnie wynagrodzenie w województwach (w zł)"}}
  })
  return fig


def other_requirements():
  others = {}

  groupped = pracuj.groupby("prawo-jazdy")
  values = groupped["company"].count()
  others["Prawo jazdy"] = [values["-1"], values["0"], values["1"]]

  groupped = pracuj.groupby("znajomość-angielskiego")
  values = groupped["company"].count()
  others["Znajomość języka angielskiego"] = [values["-1"], values["0"], values["1"]]
  
  df = pd.DataFrame(others)
  df = df.transpose()
  df.columns = ["Brak informacji", "Nie", "Tak"]
  fig = px.bar(df)
  fig.update_layout(legend_title="Czy wymagane?")
  return fig

import requests
import geopandas
import matplotlib.pyplot as plt
import zipfile

def location():
  locations = ["mazowieckie", "dolnośląskie", "małopolskie", "śląskie", "łódzkie", "wielkopolskie", "opolskie", "podlaskie", "zachodnio-pomorskie", "podkarpackie", "lubelskie", "lubuskie", "świętokrzyskie", "warmińsko-mazurskie", "kujawsko-pomorskie", "pomorskie"]
  number_of_offers = []
  for l in locations:
    pracuj[l] = pd.to_numeric(pracuj[l])
    number = 0
    for i in range(len(pracuj[l])):
      if pracuj[l][i] == 1:
        number += 1
    number_of_offers.append(number)

  url = "https://www.gis-support.pl/downloads/2022/wojewodztwa.zip"
  r = requests.get(url, allow_redirects=True)
  open('wojewodztwa.zip', 'wb').write(r.content)

  voivodeships = read_shape_from_zip("wojewodztwa.zip", "wojewodztwa")
  voivodeships = geopandas.read_file("wojewodztwa.zip")
  data = pd.DataFrame({'JPT_NAZWA_': locations, 'number_of_offers': number_of_offers})
  voivodeships = pd.merge(data, voivodeships, on='JPT_NAZWA_', how='left')
  print(voivodeships)
    
  fig, ax = plt.subplots(figsize=(10, 10))
  voivodeships.plot(column="number_of_offers", ax=ax)
  vmin, vmax = voivodeships["number_of_offers"].min(), voivodeships["number_of_offers"].max()
  sm = plt.cm.ScalarMappable(norm=plt.Normalize(vmin=vmin, vmax=vmax))
  sm.set_array([])
  fig.colorbar(sm, shrink=0.5, ax=ax)
  ax.grid(True)
  ax.set_axis_off()
  ax.set_title("Liczba ofert pracy w województwach")
  plt.tight_layout()
  plt.show()

  fig = dict({
    "data": [{"type": "bar",
              "x": locations,
              "y": number_of_offers}],
    "layout": {"title": {"text": "Liczba ofert pracy w województwach"}}
  })

  return fig

def salary_by_region():
    locations = ["mazowieckie", "dolnośląskie", "małopolskie", "śląskie", "łódzkie", "wielkopolskie", "opolskie", "podlaskie", "zachodnio-pomorskie", "podkarpackie", "lubelskie", "lubuskie", "świętokrzyskie", "warmińsko-mazurskie", "kujawsko-pomorskie", "pomorskie"]
    salaries = []
    pracuj["salary"] = pd.to_numeric(pracuj["salary"])
    for l in locations:
        pracuj[l] = pd.to_numeric(pracuj[l])
        salaries_sum = 0
        number = 0
        for i in range(len(pracuj[l])):
            if pracuj[l][i] == 1 and pracuj["salary"][i] != -1:
                number += 1
                salaries_sum += pracuj["salary"][i]
        salaries.append(salaries_sum/number)


    df = pd.DataFrame(data={"loc":locations,"sal":salaries})
    geojson = polmap
    fig = px.choropleth(
        df, geojson=geojson, color="sal",
        locations="loc", featureidkey="properties.name",
        projection="mercator", range_color=[min(salaries), max(salaries)])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def requirements():

    months = ["2021-01", "2021-02", "2021-03", "2021-04", "2021-05", "2021-06", "2021-07", "2021-08", "2021-09", "2021-10", "2021-11", "2021-12",
              "2022-01", "2022-02", "2022-03", "2022-04", "2022-05", "2022-06", "2022-07", "2022-08", "2022-09", "2022-10", "2022-11", "2022-12",
              "2023-01", "2023-02", "2023-03", "2023-04", "2023-05"
              ]
    df = pd.DataFrame(requirements, index=months)
    fig = px.line(df, title="Liczba ofert z określonymi wymaganiami", markers=True)
    fig.update_layout(xaxis_title="Czas", yaxis_title="Liczba", legend_title="Wymaganie")
    fig.show()