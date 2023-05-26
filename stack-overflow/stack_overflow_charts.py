import pandas as pd
import matplotlib.pyplot as plt

def degrees_through_years():
    df = pd.read_csv("/content/drive/MyDrive/Wizualizacja danych/stack-overflow/survey_results_public_2017.csv")
    poland_data = df[df["Country"] == "Poland"]
    levels2017 = poland_data["FormalEducation"].value_counts()
    levels2017["Associate degree"] = 0
    levels2017["NDoctoral degree"] = levels2017["Doctoral degree"]
    levels2017["Something else"] = levels2017["I prefer not to answer"]
    levels2017 = levels2017.drop(labels=["Doctoral degree", "I prefer not to answer"])
    levels2017 = levels2017.sort_index()
    print(levels2017)

    df = pd.read_csv("/content/drive/MyDrive/Wizualizacja danych/stack-overflow/survey_results_public_2018.csv")
    poland_data = df[df["Country"] == "Poland"]
    levels2018 = poland_data["FormalEducation"].value_counts()
    levels2018["Something else"] = 0
    levels2018 = levels2018.sort_index()
    print(levels2018)

    df = pd.read_csv("/content/drive/MyDrive/Wizualizacja danych/stack-overflow/survey_results_public_2019.csv")
    poland_data = df[df["Country"] == "Poland"]
    levels2019 = poland_data["EdLevel"].value_counts()
    levels2019["Something else"] = 0
    levels2019 = levels2019.sort_index()
    print(levels2019)

    df = pd.read_csv("/content/drive/MyDrive/Wizualizacja danych/stack-overflow/survey_results_public_2020.csv")
    poland_data = df[df["Country"] == "Poland"]
    levels2020 = poland_data["EdLevel"].value_counts()
    levels2020["Something else"] = 0
    levels2020 = levels2020.sort_index()
    print(levels2020)

    df = pd.read_csv("/content/drive/MyDrive/Wizualizacja danych/stack-overflow/survey_results_public_2021.csv")
    poland_data = df[df["Country"] == "Poland"]
    levels2021 = poland_data["EdLevel"].value_counts()
    levels2021["I have never completed any formal education"] = 0
    levels2021 = levels2021.sort_index()
    print(levels2021)

    df = pd.read_csv("/content/drive/MyDrive/Wizualizacja danych/stack-overflow/survey_results_public_2022.csv")
    poland_data = df[df["Country"] == "Poland"]
    levels2022 = poland_data["EdLevel"].value_counts()
    levels2022["I have never completed any formal education"] = 0
    levels2022 = levels2022.sort_index()
    print(levels2022)

    years = [2017, 2018, 2019, 2020, 2021, 2022]
    #plt.stackplot(years, [levels2017.values.tolist(), levels2018.values.tolist(), levels2019.values.tolist(), levels2020.values.tolist(), levels2021.values.tolist(), levels2022.values.tolist()], labels=["Magister", "Licencjat"])
    #plt.show()

degrees_through_years()