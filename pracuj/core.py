import json
import re
import pandas as pd
import urllib
import urllib.request
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import csv
import requests
import time
import numpy as np
import threading
import atexit


tagi = np.loadtxt("./config/search_tags.txt",dtype=str)
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
delay = 5

class Loader:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.last_page = None
        self.last_year = None
        self.last_month = None
        if(not self.file_name):
            self.file_name = "should_be_empty.json"
        with open('./config/pracuj_config.json', 'r') as file:
            self.conf = json.load(file)
            print(self.conf)
        atexit.register(self.save_progress)
        self.open_file()
        self.tags = set()
        self.stats = {}
        self.auto_save_value = self.conf["auto_save_every_n_pages"]
        for i in range(2014,2024):
            self.stats[i]=[{"pages":0,"all_offers":0,"matched_offers":0} for _ in range (12)]

    def open_file(self):
        try:
            out_file = open("./data/"+self.file_name,"r",encoding="utf-8")
            self.load_file(out_file)
            out_file.close()
        except Exception as ex:
            print("Could not open json file: "+self.file_name+";",ex)

    def load_file(self,file):
        if file != None:
            self.data = json.load(file)
        else:
            print("Error while loading json file!!!!!!!! (plik prawdobodobnie nie istnieje)")
            exit()
    def url(self,rok,miesiac,strona):
        return str(f'https://archiwum.pracuj.pl/archive/offers?Year={rok}&Month={miesiac}&PageNumber={strona}')

    def get(self,url):
        res = requests.get(url,headers=hdr,allow_redirects=True)
        while res.status_code != 200:
            print("                                                     Status code: ",res.status_code)
            print(f"Requesting again in {self.conf['delay']} seconds...")
            time.sleep(self.conf['delay'])
            res = requests.get(url,headers=hdr,allow_redirects=True)
        res.encoding = 'utf-8'
        
        return res

    def check_tags(self,title):
        for wyraz in title.split():
            if( wyraz.lower() in tagi):
                return True
        return False


    def scrap(self,page,date):
        print("scrap not implemented")

    def load_data(self):
        inc = -1
        
        page = self.conf["start_from_page"]
        year = self.conf[ "start_from_year"]
        month = self.conf[ "start_from_month"]

        if self.conf["search_from_oldest_to_newer"]:
            inc = 1
        if self.conf["use_save_file_if_exists"]:
            with open('./config/last_session.json', 'r') as file:
                save = json.load(file)
                if save["page"]:
                    page = save["page"]

                if save["month"]:
                    month = save["month"]

                if save["year"]:
                    year = save["year"]

        current_month = self.conf["current_month"]
        current_year = self.conf["current_year"]
        while year<= current_year and year>= 2014:
            self.last_year = year
            print(f"Scraping for year {year}")
            if year == current_year:
                while month <= current_month and month >0:
                    self.last_month = month
                    print(f"Scraping for month {month}")
                    self.load_all_pages(month,year,page)
                    page = 1
                    month += inc
                    print("Scraping next month!!")

            else:     
                while month <= 12 and month >0:
                    self.last_month = month
                    print(f"Scraping for month {month}")
                    self.load_all_pages(month,year,page)
                    month += inc
                    page = 1
                    print("Scraping next month!!")
            if inc>0:
                month = 0
            else:
                month = 12
            year+=inc
            print("Scraping next year!!")
        
    def load_all_pages(self,month,year,page=1):        
        print("Loading data...")
        # executor = ThreadPoolExecutor(8)
        does_next_exist = True
        while page<3000 and does_next_exist:
            print(f'Pobieranie strony {page} m:{month},y:{year}')
            resp = self.get(self.url(year,month,page))
            # future = executor.submit(self.scrap, (processed_page),(year,month,page))
            # future.result()
            print(f'Parsowanie strony {page}')
            processed_page = BeautifulSoup(resp.text, "html.parser")
            retry_amount = 3
            i = 0

            while processed_page.find(class_="offers_empty") and i < retry_amount-1: 
                print("             Checking for page end one more time")
                resp = self.get(self.url(year,month,page))
                processed_page = BeautifulSoup(resp.text, "html.parser")

                i+=1
            if(processed_page.find(class_="offers_empty")):
                does_next_exist=False
                print("                 page does not exist! ",self.url(year,month,page))
                with open("temps.txt", 'w+', encoding="utf-8") as file:
                    file.write(resp.text)
            else:
                self.scrap(processed_page,(year,month,page))
                page+=1
                if (page%self.auto_save_value)==0:
                    self.save_progress()
                self.last_page=page
                self.stats[year][month-1]["pages"] = page

    def save_progress(self):
        if 'stats' in self.conf:
            staty_stare = self.conf['stats']
            for key in staty_stare.keys():
                for i in range(12):
                    self.stats[key][i] = staty_stare[key][i]
        progress = {
            'page':self.last_page,
            'month':self.last_month,
            'year':self.last_year,
            'stats':self.stats
        }
        with open('./config/last_session.json', 'w+') as file:
            json.dump(progress, file,indent=4)
        with open('./data/'+self.file_name, 'w', encoding="utf-8") as file:
            json.dump(self.data, file,indent=self.conf["data_indent"],ensure_ascii=False)
        with open('./config/pracuj_attribute_names.txt', 'w+') as file:
            for element in self.tags:
                file.write(str(element) + "\n")

import asyncio

class Loader_Async:
    
    async def req(self,num):
        print(f"Working {num}")
        await asyncio.sleep(num)
        print(f"Finished {num}")
        if num < 12:
            x = asyncio.create_task(self.req(num+3))
            await x

    async def async_loop(self):
        a = asyncio.create_task(self.req(1))
        b = asyncio.create_task(self.req(2))
        c = asyncio.create_task(self.req(3))
        await a
        await b
        await c
    def start(self):
        asyncio.run(self.async_loop())

    

if __name__ ==  "__main__":
    loader = Loader_Async()
    loader.start()