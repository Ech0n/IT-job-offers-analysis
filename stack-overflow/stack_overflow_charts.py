import pandas as pd
import matplotlib.pyplot as plt

# data_source = "/content/drive/MyDrive/Wizualizacja danych/stack-overflow/"
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

def degrees_through_years():
    levels2017 = df2017["FormalEducation"].value_counts()
    levels2017["NDoctoral degree"] = levels2017["Doctoral degree"]
    levels2017["Something else"] = levels2017["I prefer not to answer"]
    levels2017 = levels2017.drop(labels=["Doctoral degree", "I prefer not to answer"])
    levels2017 = levels2017.sort_index()

    levels2018 = df2018["FormalEducation"].value_counts()
    levels2018["Something else"] = levels2018["Associate degree"]
    levels2018 = levels2018.drop(labels=["Associate degree"])
    levels2018 = levels2018.sort_index()

    levels2019 = df2019["EdLevel"].value_counts()
    levels2019["Something else"] = levels2019["Associate degree"]
    levels2019 = levels2019.drop(labels=["Associate degree"])
    levels2019 = levels2019.sort_index()

    levels2020 = df2020["EdLevel"].value_counts()
    levels2020["Something else"] = levels2020["Associate degree (A.A., A.S., etc.)"]
    levels2020 = levels2020.drop(labels=["Associate degree (A.A., A.S., etc.)"])
    levels2020 = levels2020.sort_index()

    levels2021 = df2021["EdLevel"].value_counts()
    levels2021["I have never completed any formal education"] = 0
    levels2021["Something else"] += levels2021["Associate degree (A.A., A.S., etc.)"]
    levels2021 = levels2021.drop(labels=["Associate degree (A.A., A.S., etc.)"])
    levels2021 = levels2021.sort_index()

    levels2022 = df2022["EdLevel"].value_counts()
    levels2022["I have never completed any formal education"] = 0
    levels2022["Something else"] += levels2022["Associate degree (A.A., A.S., etc.)"]
    levels2022 = levels2022.drop(labels=["Associate degree (A.A., A.S., etc.)"])
    levels2022 = levels2022.sort_index()

    years = [2017, 2018, 2019, 2020, 2021, 2022]
    data = []
    for i in range(9):
      data.append([])
      data[i].append(levels2017.values[i])
      data[i].append(levels2018.values[i])
      data[i].append(levels2019.values[i])
      data[i].append(levels2020.values[i])
      data[i].append(levels2021.values[i])
      data[i].append(levels2022.values[i])
    
    keys = ["Licencjackie / inżynierskie", "Brak", "Magisterskie", "Doktorskie", "Podstawowe", "Wyższe niż doktorskie", "Średnie", "Nieukończone studia", "Inne"]
    df = pd.DataFrame()
    for i in range(9):
      df[keys[i]] = data[i]

    keys = ["Brak", "Podstawowe", "Średnie", "Nieukończone studia", "Licencjackie / inżynierskie", "Magisterskie", "Doktorskie", "Wyższe niż doktorskie", "Inne"]
    df = df[keys]
    df = df.divide(df.sum(axis=1), axis=0)
    plt.stackplot(years, df.values.T, labels=keys)
    plt.title("Udział w rynku osób z poszczególnym wykształceniem w latach 2017-2022")
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

degrees_through_years()
