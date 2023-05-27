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
        super().__init__()
        self.out_file_name = './data/pracuj_detailed.csv'
        with open(self.out_file_name, 'w+',newline='', encoding='utf-8') as f:
            f.truncate(0)
    def load_offer(self,url):
        resp = self.get(url)
        data = [0 for _ in range(10)]
        processed_page = BeautifulSoup(resp.text, "html.parser")
        name = processed_page.find(class_="offer-viewkHIhn3").text
        data[0] = name
        attrs = processed_page.find_all(class_="offer-viewXo2dpV")
        for i,x in enumerate(attrs):
            if(i+1<10):
                data[i+1]= x.text
        self.lock.acquire()
        try:
            with open('./data/pracuj_detailed.csv', 'a+',newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(data)
        finally:
            self.lock.release()
    def scrap(self,page):
        print("_")
        for a in page.find_all(class_="offers_item"):
            x = a.find(class_="offers_item_link_cnt_part")
            if x and self.check_tags(x.text):
                x = a.find(class_="offers_item_link")
                if x:
                    self.load_offer(x.get("href"))    
        print("Done processing page ")

    # def load_data(self):
    #     with open('./data/pracuj_detailed.csv', 'w+',newline='', encoding='utf-8') as f:
    #         f.truncate(0)
    #     print("Loading data...")
    #     executor = ThreadPoolExecutor(8)
    #     pages = []
    #     oferty = []
    #     page = 1
    #     does_next_exist = True
    #     while page<3000 and does_next_exist:
    #         print(f'Pobieranie strony {page}')
    #         resp = self.get(self.page_url(2022,1,page))
    #         print(f'Parsowanie strony {page}')
    #         processed_page = BeautifulSoup(resp.text, "html.parser")
    #         future = executor.submit(self.scrap, (processed_page))
    #         future.result()
    #         if(processed_page.find(class_="offers_nav_next") == None):
    #             does_next_exist=False
    #         page+=1
        
        
if __name__ ==  "__main__":
    loader = Detailed_Loader()
    loader.load_data()