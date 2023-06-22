import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import geopandas
import re
import zipfile
import os
import requests
import warnings

file_columns = open("../data/kolumny_pracuj.txt", "r", encoding="utf-8")
columns_list = []
for line in file_columns:
  columns_list = line.split()

pracuj = pd.read_csv("../data/pracuj.csv", encoding="utf-8", dtype=str, delimiter=";", names=columns_list, header=None, low_memory=False)

def requirements():
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
          print(p[c])
          if p[c] == "1":
            number_of_requirements += 1
        requirements[c].append(number_of_requirements)

      pracuj3 = pracuj2[pracuj2["rok"] == "2022"]
      for m in range(1, 13):
        pracuj4 = pracuj3[pracuj3["month"] == m]
        number_of_requirements = 0
        for _, p in pracuj4.iterrows():
          if p[c] == "1":
            number_of_requirements += 1
        requirements[c].append(number_of_requirements)

      pracuj3 = pracuj2[pracuj2["rok"] == "2023"]
      for m in range(1, 13):
        pracuj4 = pracuj3[pracuj3["month"] == m]
        number_of_requirements = 0
        for _, p in pracuj4.iterrows():
          if p[c] == "1":
            number_of_requirements += 1
        requirements[c].append(number_of_requirements)
  #print(requirements)

requirements()
