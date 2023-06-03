import pandas as pd
import matplotlib.pyplot as plt

def degrees_through_years():
    df = pd.read_csv("/content/drive/MyDrive/Wizualizacja danych/stack-overflow/survey_results_public_2017.csv")
    poland_data = df[df["Country"] == "Poland"]
    levels2017 = poland_data["FormalEducation"].value_counts()
    levels2017["NDoctoral degree"] = levels2017["Doctoral degree"]
    levels2017["Something else"] = levels2017["I prefer not to answer"]
    levels2017 = levels2017.drop(labels=["Doctoral degree", "I prefer not to answer"])
    levels2017 = levels2017.sort_index()

    df = pd.read_csv("/content/drive/MyDrive/Wizualizacja danych/stack-overflow/survey_results_public_2018.csv")
    poland_data = df[df["Country"] == "Poland"]
    levels2018 = poland_data["FormalEducation"].value_counts()
    levels2018["Something else"] = levels2018["Associate degree"]
    levels2018 = levels2018.drop(labels=["Associate degree"])
    levels2018 = levels2018.sort_index()

    df = pd.read_csv("/content/drive/MyDrive/Wizualizacja danych/stack-overflow/survey_results_public_2019.csv")
    poland_data = df[df["Country"] == "Poland"]
    levels2019 = poland_data["EdLevel"].value_counts()
    levels2019["Something else"] = levels2019["Associate degree"]
    levels2019 = levels2019.drop(labels=["Associate degree"])
    levels2019 = levels2019.sort_index()

    df = pd.read_csv("/content/drive/MyDrive/Wizualizacja danych/stack-overflow/survey_results_public_2020.csv")
    poland_data = df[df["Country"] == "Poland"]
    levels2020 = poland_data["EdLevel"].value_counts()
    levels2020["Something else"] = levels2020["Associate degree (A.A., A.S., etc.)"]
    levels2020 = levels2020.drop(labels=["Associate degree (A.A., A.S., etc.)"])
    levels2020 = levels2020.sort_index()

    df = pd.read_csv("/content/drive/MyDrive/Wizualizacja danych/stack-overflow/survey_results_public_2021.csv")
    poland_data = df[df["Country"] == "Poland"]
    levels2021 = poland_data["EdLevel"].value_counts()
    levels2021["I have never completed any formal education"] = 0
    levels2021["Something else"] += levels2021["Associate degree (A.A., A.S., etc.)"]
    levels2021 = levels2021.drop(labels=["Associate degree (A.A., A.S., etc.)"])
    levels2021 = levels2021.sort_index()

    df = pd.read_csv("/content/drive/MyDrive/Wizualizacja danych/stack-overflow/survey_results_public_2022.csv")
    poland_data = df[df["Country"] == "Poland"]
    levels2022 = poland_data["EdLevel"].value_counts()
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