import json
import re
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import csv
import threading
import requests
import time
from core import Loader


url = "https://archiwum.pracuj.pl/archive/offers?Year=2023&Month=1&PageNumber="
tagi = ["software","programmer","programista"]
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
delay = 5
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

    def load_offer(self,url,date):
        resp = self.get(url)
        data = [0 for _ in range(10)]
        processed_page = BeautifulSoup(resp.text, "html.parser")
        name = processed_page.find(class_="offer-viewkHIhn3").text

        data[0] = name
        attrs = processed_page.find_all(attrs={"data-scroll-id":True})
        company = processed_page.find("h2",{"data-scroll-id":"employer-name"}).text
        dane = {}
        for i,x in enumerate(attrs):
            if(i+1<10):
                data[i+1]= x.text
            dane[x.get("data-scroll-id")] = x.text
        self.lock.acquire()
        try:
            with open('./data/pracuj_detailed.csv', 'a+',newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(data)
            self.data[date[0]][date[1]][company] = {}
            self.data[date[0]][date[1]][company][name] = dane
        finally:
            self.lock.release()
    def print_attrs(self,x):
        print("Printing attrs:")
        for y in x:
            if y.text:
                print("   "+y.text,end=" ")
            if y.get("data-test"):
                o = y.get("data-test")
                print("||| "+o,end=" ")
                self.tags.add(o)

            print(" ")

    def scrap(self,page,date):
        print("_")
        if date[0] not in self.data:
            self.data[date[0]] = {}
            self.data[date[0]][date[1]] = {}
        elif date[1] not in self.data[date[0]]:
            self.data[date[0]][date[1]] = {}
    
        for a in page.find_all(class_="offers_item"):
            x = a.find(class_="offers_item_link_cnt_part")
            if x and self.check_tags(x.text):
                x = a.find(class_="offers_item_link")
                if x:
                    self.load_offer(x.get("href"),date)    
        print("Done processing page ")

        
        
if __name__ ==  "__main__":
    loader = Detailed_Loader()
    loader.load_data()