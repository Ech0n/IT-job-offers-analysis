import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

file_columns = open("kolumny_pracuj.txt", "r", encoding="utf-8")
columns_list = []
for line in file_columns:
  columns_list = line.split()

pracuj = pd.read_csv("../data/pracuj.csv", encoding="utf-8", dtype=str, delimiter=";", names=columns_list, header=None, low_memory=False)

def number_of_offers():
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
  fig.show()

def types_of_contract():
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
  
  pio.show(fig)

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
  
  fig = dict({
    "data": [{"type": "bar",
              "x": locations,
              "y": number_of_offers}],
    "layout": {"title": {"text": "Liczba ofert pracy w województwach"}}
  })
  
  pio.show(fig)

def experience_level():
  level = ["-1", "intern", "junior", "mid", "senior"]
  d = dict()
  for l in level:
    d[l] = 0
  for i in range(len(pracuj["experience-level"])):
    d[pracuj["experience-level"][i]] += 1
  d.pop("-1")
  k = list(d.keys())
  v = list(d.values())
  
  fig = px.pie(values=v, names=k)
  fig.show()

number_of_offers()
types_of_contract()
location()
experience_level()
