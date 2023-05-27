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


# url = "https://archiwum.pracuj.pl/archive/offers?Year=2023&Month=1&PageNumber="
# tagi = ["software","programmer","programista"]
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
        with open('./config/pracuj_config.json', 'r') as file:
            self.conf = json.load(file)
            print(self.conf)
        atexit.register(self.save_progress)
    def url(self,rok,miesiac,strona):
        return str(f'https://archiwum.pracuj.pl/archive/offers?Year={rok}&Month={miesiac}&PageNumber={strona}')

    def get(self,url):
        res = requests.get(url,headers=hdr)
        while res.status_code != 200:
            print("Status code: ",res.status_code)
            print(f"Requesting again in {self.conf['delay']} seconds...")
            time.sleep(self.conf['delay'])
            res = requests.get(url,headers=hdr)
        return res

    def check_tags(self,title):
        for wyraz in title.split():
            if( wyraz.lower() in tagi):
                return True
        return False


    def scrap(self,page):
        print("scrap not implemented")

    def load_data(self):
        inc = -1
        if self.conf["search_from_oldest_to_newer"]:
            inc = 1
        page = self.conf["start_from_page"]
        year = self.conf[ "start_from_year"]
        month = self.conf[ "start_from_month"]
        current_month = self.conf["current_month"]
        current_year = self.conf["current_year"]
        while year<= current_year and year>= 2014:
            print(f"Scraping for year {year}")
            if year == current_year:
                while month <= current_month and month >0:
                    print(f"Scraping for month {month}")
                    self.load_all_pages(month,year)
                    month += inc
                    print("Scraping next month!!")

            else:     
                while month <= 12 and month >0:
                    print(f"Scraping for month {month}")
                    self.load_all_pages(month,year)
                    month += inc
                    print("Scraping next month!!")

            if inc>0:
                month = 0
            else:
                month = 12
            year+=inc
            print("Scraping next year!!")
        
    def load_all_pages(self,month,year,page=1):

        
        print("Loading data...")
        executor = ThreadPoolExecutor(8)
        page = 1984
        does_next_exist = True
        while page<3000 and does_next_exist:
            print(f'Pobieranie strony {page}')
            resp = self.get(self.url(year,month,page))
            print(f'Parsowanie strony {page}')
            processed_page = BeautifulSoup(resp.text, "html.parser")
            future = executor.submit(self.scrap, (processed_page))
            future.result()
            if(processed_page.find(class_="offers_nav_next") == None):
                does_next_exist=False
            page+=1
            self.last_page=page
    
    def save_progress(self):
        progress = {
            'page':self.last_page,
            'month':self.last_month,
            'year':self.last_year
        }
        with open('./config/last_session.json', 'w+') as file:
            json.dump(progress, file)

loader = None
if __name__ ==  "__main__":
    with Loader() as loader:
        loader.load_data()
