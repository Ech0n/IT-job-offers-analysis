import pandas as pd
import matplotlib.pyplot as plt

#data_source = "/content/drive/MyDrive/Wizualizacja danych/stack-overflow/"
data_source = "../data/stack-overflow/"

df2011 = pd.read_csv(data_source + "2011 Stack Overflow Survey Results.csv", encoding="cp1252")
df2012 = pd.read_csv(data_source + "2012 Stack Overflow Survey Results.csv", encoding="cp1252")
df2013 = pd.read_csv(data_source + "2013 Stack Overflow Survey Responses.csv", low_memory=False)
df2014 = pd.read_csv(data_source + "2014 Stack Overflow Survey Responses.csv")
df2015 = pd.read_csv(data_source + "2015 Stack Overflow Developer Survey Responses.csv", low_memory=False, skiprows=[0])
df2016 = pd.read_csv(data_source + "2016 Stack Overflow Survey Responses.csv")
df2017 = pd.read_csv(data_source + "survey_results_public_2017.csv")
df2018 = pd.read_csv(data_source + "survey_results_public_2018.csv", low_memory=False)
df2019 = pd.read_csv(data_source + "survey_results_public_2019.csv")
df2020 = pd.read_csv(data_source + "survey_results_public_2020.csv")
df2021 = pd.read_csv(data_source + "survey_results_public_2021.csv")
df2022 = pd.read_csv(data_source + "survey_results_public_2022.csv")

df2011 = df2011[df2011["What Country or Region do you live in?"] == "Poland"]
df2012 = df2012[df2012["What Country or Region do you live in?"] == "Poland"]
df2013 = df2013[df2013["What Country or Region do you live in?"] == "Poland"]
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

def gender_through_years():
    gender2014 = df2014["What is your gender?"].value_counts()

    gender2015 = df2015["Gender"].value_counts()
    gender2015["Prefer not to disclose"] += gender2015["Other"]
    gender2015 = gender2015.drop(labels=["Other"])

    gender2016 = df2016["gender"].value_counts()
    gender2016["Prefer not to disclose"] += gender2016["Other"]
    gender2016 = gender2016.drop(labels=["Other"])

    gender2017 = df2017["Gender"].value_counts()
    for g in gender2017.index:
      if g != "Male" and g != "Female" and g != "Other":
        gender2017["Other"] += gender2017[g]
        gender2017 = gender2017.drop(labels=[g])

    gender2018 = df2018["Gender"].value_counts()
    gender2018["Other"] = 0
    for g in gender2018.index:
      if g != "Male" and g != "Female" and g != "Other":
        gender2018["Other"] += gender2018[g]
        gender2018 = gender2018.drop(labels=[g])

    gender2019 = df2019["Gender"].value_counts()
    gender2019["Other"] = 0
    for g in gender2019.index:
      if g != "Man" and g != "Woman" and g != "Other":
        gender2019["Other"] += gender2019[g]
        gender2019 = gender2019.drop(labels=[g])

    gender2020 = df2020["Gender"].value_counts()
    gender2020["Other"] = 0
    for g in gender2020.index:
      if g != "Man" and g != "Woman" and g != "Other":
        gender2020["Other"] += gender2020[g]
        gender2020 = gender2020.drop(labels=[g])

    gender2021 = df2021["Gender"].value_counts()
    gender2021["Other"] = 0
    for g in gender2021.index:
      if g != "Man" and g != "Woman" and g != "Other":
        gender2021["Other"] += gender2021[g]
        gender2021 = gender2021.drop(labels=[g])

    gender2022 = df2022["Gender"].value_counts()
    gender2022["Other"] = 0
    for g in gender2022.index:
      if g != "Man" and g != "Woman" and g != "Other":
        gender2022["Other"] += gender2022[g]
        gender2022 = gender2022.drop(labels=[g])

    data = []
    for i in range(3):
      data.append([])
      data[i].append(gender2014.values[i])
      data[i].append(gender2015.values[i])
      data[i].append(gender2016.values[i])
      data[i].append(gender2017.values[i])
      data[i].append(gender2018.values[i])
      data[i].append(gender2019.values[i])
      data[i].append(gender2020.values[i])
      data[i].append(gender2021.values[i])
      data[i].append(gender2022.values[i])
    
    keys = ["Mężczyźni", "Kobiety", "Inne / odmowa odp."]
    df = pd.DataFrame()
    for i in range(3):
      df[keys[i]] = data[i]
    df = df[keys]
    df = df.divide(df.sum(axis=1), axis=0)
    years = range(2014, 2023)
    plt.stackplot(years, df.values.T, labels=keys)
    plt.title("Rozkład płci w latach 2014-2022")
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    plt.show()

def remote_work():
    remote2014 = df2014["Do you work remotely?"].value_counts()
    remote2014 = pd.Series([remote2014["Full-time Remote"], remote2014["Part-time Remote"], remote2014["Never"], remote2014["Occasionally"]], index=["Full-time Remote", "Part-time Remote", "Never", "Occasionally"])
    keys = ["Tylko zdalnie", "Hybrydowo", "Tylko stacjonarnie", "Okazjonalnie zdalnie"]
    plt.pie(remote2014.values, labels=keys) #colors=["gray", "#c93636", "#405ebf", "#cba034"]
    plt.title("Praca zdalna w roku 2014")
    plt.show()
    print(remote2014)

    remote2022 = df2022["RemoteWork"].value_counts()
    keys = ["Tylko zdalnie", "Hybrydowo", "Tylko stacjonarnie"]
    plt.pie(remote2022.values, labels=keys)
    plt.title("Praca zdalna w roku 2022")
    plt.show()

def company_size():
    size2022 = df2022["OrgSize"].value_counts()
    size2022 = size2022.drop(labels=["I don’t know"])
    size2022 = pd.Series([size2022["Just me - I am a freelancer, sole proprietor, etc."], size2022["2 to 9 employees"], size2022["10 to 19 employees"], size2022["20 to 99 employees"], size2022["100 to 499 employees"],
                          size2022["500 to 999 employees"], size2022["1,000 to 4,999 employees"], size2022["5,000 to 9,999 employees"], size2022["10,000 or more employees"]],
                         index=["Just me - I am a freelancer, sole proprietor, etc.", "2 to 9 employees", "10 to 19 employees", "20 to 99 employees", "100 to 499 employees", "500 to 999 employees",
                                "1,000 to 4,999 employees", "5,000 to 9,999 employees", "10,000 or more employees"])
    keys = ["Własna (jednoosobowa) firma", "2 do 9", "10 do 19", "20 do 99", "100 do 499", "500 do 999", "1,000 do 4,999", "5000 do 9999", "10,000 i więcej"]
    plt.pie(size2022.values, labels=keys, colors=("#cce0ff", "#99c2ff", "#66a3ff", "#3385ff", "#0066ff", "#0052cc", "#003d99", "#002966", "#001433"))
    plt.suptitle("Wielkość firm w których pracowali programiści w 2022 roku")
    plt.title("Wykres przedstawia liczbę pracowników w firmach", fontsize=10)
    plt.show()
    
degrees_through_years()
gender_through_years()
remote_work()
company_size()