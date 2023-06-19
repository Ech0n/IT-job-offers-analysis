import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

file_columns = open("kolumny_pracuj.txt", "r", encoding="cp1252")
columns_list = []
for line in file_columns:
  columns_list = line.split()

pracuj = pd.read_csv("./data/pracuj.csv", encoding="utf-8", dtype=str, delimiter=";", names=columns_list, header=None, low_memory=False)

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
                  y=["2019", "2020", "2022", "2023"],
                  color_continuous_scale="Blues"
                  )
  fig.show()

number_of_offers()