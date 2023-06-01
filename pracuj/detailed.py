import json
import re
import pandas as pd
from bs4 import BeautifulSoup
import requests
from core import Loader
import traceback
import sys
import asyncio
url = "https://archiwum.pracuj.pl/archive/offers?Year=2023&Month=1&PageNumber="
tagi = ["software","programmer","programista"]
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
delay = 5
excluded_tags = ["about-us-extended","about-us-extended-1","about-us-1","about-us-extension","about-us-extension-1","about-us-description-1"]
listed_classes= ["offer-view7CmY-p offer-viewF0WZVq","offer-viewEX0Eq-","offer-view6lWuAT","offer-viewehUktj"]
class Detailed_Loader(Loader):
    def __init__(self) -> None:
        self.file_name = "detailed.json"
        super().__init__()
        self.out_file_name = './data/pracuj_detailed.csv'
        with open(self.out_file_name, 'w+',newline='', encoding='utf-8') as f:
            f.truncate(0)

        with open("./config/pracuj_attribute_names.txt","r") as file:
            self.attr_tags = []
            for line in file.readlines():
                self.attr_tags.append(line)
    def get_element_contents(self,element):
        contents = []
        for child in element.children:
            contents.append(child.text)
        return contents
    def get_salary_contents(self,element):
        contents = []
        for child in element.children:
            contract = {}
            min = child.find(class_="offer-viewZGJhIB")
            if min:
                contract["min"] = min.text
            max = child.find(class_="offer-viewYo2KTr")
            if max:
                contract["max"] = max.text
            unit = child.find(class_="offer-viewSGW6Yi")
            if unit:
                contract["unit"] = unit.text
            typ = child.find(class_="offer-vieweHKpRl")
            if typ:
                contract["type"] = typ.text
            contents.append(contract)
        return contents
    def load_offer(self,url,date):
        resp = self.get(url)
        data = [0 for _ in range(10)]
        processed_page = BeautifulSoup(resp.text, "html.parser")
        name = processed_page.find(class_="offer-viewkHIhn3")
        if(name==None):
            print("Napotkano wadliwom oferte: ",url)
            return
        name = name.text
        data[0] = name
        attrs = processed_page.find_all(attrs={"data-scroll-id":True})
        company = processed_page.find("h2",{"data-scroll-id":"employer-name"}).contents[0]
        dane = {"localization":[]}
        for i,x in enumerate(attrs):
            if(i+1<10):
                data[i+1]= x.text

            tag = x.get("data-scroll-id")
            if(tag=="workplaces"):
                dane["localization"].append(x.contents[-1].text)
            elif tag=="contract-types-salary":
                dane["contract"] = self.get_salary_contents(x)
            else:
                if not any(str(tag)== ab for ab in excluded_tags):
                    found_list = False
                    i = 0
                    while (not found_list) and i < len(listed_classes):
                        class_name = listed_classes[i]
                        lista = x.find(class_=class_name)
                        if(lista):
                            found_list=True
                            elementy = self.get_element_contents(lista)
                            dane[tag] = elementy
                        i+=1
                    if not found_list:
                        dane[tag] = x.text
                    # if lista != None:
                    #     elementy = self.get_element_contents(lista)
                    #     # print("Dodaje liste typu :" ,"\n",elementy)
                    #     dane[tag] = elementy
                    # else:
                    #     lista = x.find(class_="offer-view6lWuAT")
                    #     if lista != None:
                    #         elementy = self.get_element_contents(lista)
                    #         # print("Dodaje liste typu :" ,"\n",elementy)
                    #         dane[tag] = elementy
                    #     else:
                    #         dane[tag] = x.text
                        
            self.tags.add(tag)
        self.lock.acquire()
        try:
            # with open('./data/pracuj_detailed.csv', 'a+',newline='', encoding='utf-8') as f:
            #     writer = csv.writer(f)
            #     writer.writerow(data)
            self.data[date[0]][date[1]][company] = {}
            self.data[date[0]][date[1]][company][name] = dane
        finally:
            self.lock.release()

    async def load_offer_async(self,url,date):
        resp = await self.get_async(url)
        data = [0 for _ in range(10)]
        processed_page = BeautifulSoup(resp, "html.parser")
        name = processed_page.find(class_="offer-viewkHIhn3")
        if(name==None):
            print("Napotkano wadliwom oferte: ",url)
            return
        name = name.text
        data[0] = name
        attrs = processed_page.find_all(attrs={"data-scroll-id":True})
        company = processed_page.find("h2",{"data-scroll-id":"employer-name"}).contents[0]
        dane = {"localization":[]}
        for i,x in enumerate(attrs):
            if(i+1<10):
                data[i+1]= x.text

            tag = x.get("data-scroll-id")
            if(tag=="workplaces"):
                dane["localization"].append(x.contents[-1].text)
            elif tag=="contract-types-salary":
                dane["contract"] = self.get_salary_contents(x)
            else:
                if not any(str(tag)== ab for ab in excluded_tags):
                    found_list = False
                    i = 0
                    while (not found_list) and i < len(listed_classes):
                        class_name = listed_classes[i]
                        lista = x.find(class_=class_name)
                        if(lista):
                            found_list=True
                            elementy = self.get_element_contents(lista)
                            dane[tag] = elementy
                        i+=1
                    if not found_list:
                        dane[tag] = x.text
                    # if lista != None:
                    #     elementy = self.get_element_contents(lista)
                    #     # print("Dodaje liste typu :" ,"\n",elementy)
                    #     dane[tag] = elementy
                    # else:
                    #     lista = x.find(class_="offer-view6lWuAT")
                    #     if lista != None:
                    #         elementy = self.get_element_contents(lista)
                    #         # print("Dodaje liste typu :" ,"\n",elementy)
                    #         dane[tag] = elementy
                    #     else:
                    #         dane[tag] = x.text
                        
            self.tags.add(tag)
        self.lock.acquire()
        try:
            # with open('./data/pracuj_detailed.csv', 'a+',newline='', encoding='utf-8') as f:
            #     writer = csv.writer(f)
            #     writer.writerow(data)
            self.data[date[0]][date[1]][company] = {}
            self.data[date[0]][date[1]][company][name] = dane
        finally:
            self.lock.release()

    def scrap(self,page,date):
        print("Started processing page ")
        if date[0] not in self.data:
            self.data[date[0]] = {}
            self.data[date[0]][date[1]] = {}
        elif date[1] not in self.data[date[0]]:
            self.data[date[0]][date[1]] = {}
    
        for a in page.find_all(class_="offers_item"):
            x = a.find_all(class_="offers_item_link_cnt_part")
            if x[0] and x[0].text and self.check_tags(x[0].text):
                company = x[1].text
                stanowisko = x[0].text
                if company in self.data[date[0]][date[1]].keys() and stanowisko in self.data[date[0]][date[1]][company].keys():
                    self.data[date[0]][date[1]][company][stanowisko]["localization"].append(a.find(class_="offers_item_desc_loc").text)
                    print(".",end="")
                else:
                    print("+",end="")
                    x = a.find(class_="offers_item_link")
                    if x:
                        self.load_offer(x.get("href"),date)    
                        self.stats[date[0]][date[1]]["matched_offers"] += 1
            try:
                self.stats[date[0]][date[1]]["all_offers"] +=1
            except Exception as ex:
                print(f"Had troubles saving stats at self.stats[{date[0]}][{int(date[1])-1}][\"all_offers\"];",ex)
                exit()
        print(" ")
        print("Done processing page ")

    async def scrap_async(self,page,date):
        print("Started processing page ")
        if date[0] not in self.data:
            self.data[date[0]] = {}
            self.data[date[0]][date[1]] = {}
        elif date[1] not in self.data[date[0]]:
            self.data[date[0]][date[1]] = {}
    
        for a in page.find_all(class_="offers_item"):
            x = a.find_all(class_="offers_item_link_cnt_part")
            if x[0] and x[0].text and self.check_tags(x[0].text):
                company = x[1].text
                stanowisko = x[0].text
                if company in self.data[date[0]][date[1]].keys() and stanowisko in self.data[date[0]][date[1]][company].keys():
                    self.data[date[0]][date[1]][company][stanowisko]["localization"].append(a.find(class_="offers_item_desc_loc").text)
                    print(".",end="")
                else:
                    print("+",end="")
                    x = a.find(class_="offers_item_link")
                    if x:
                        await self.load_offer_async(x.get("href"),date)    
                        self.stats[date[0]][date[1]]["matched_offers"] += 1
            try:
                self.stats[date[0]][date[1]]["all_offers"] +=1
            except Exception as ex:
                print(f"Had troubles saving stats at self.stats[{date[0]}][{date[1]-1}][\"all_offers\"];",ex)
                exit()
        print(" ")
        print("Done processing page ")
        
        
if __name__ ==  "__main__":
    loop = asyncio.get_event_loop()
    try:
        loader = Detailed_Loader()
        loader.start()
    except KeyboardInterrupt:
        print("Program exited;\n Ctrl + C caught!")

    except Exception:
        traceback.print_exc(file=sys.stdout)
