import json
import re
import pandas as pd
import urllib
import urllib.request
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import csv



url = "https://archiwum.pracuj.pl/archive/offers?Year=2023&Month=1&PageNumber="
tagi = ["software","programmer","programista"]
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
class Loader:
    def url(self,rok,miesiac,strona):
        return str(f'https://archiwum.pracuj.pl/archive/offers?Year={rok}&Month={miesiac}&PageNumber={strona}')


    def check_tags(self,title):
        for wyraz in title.split():
            if( wyraz.lower() in tagi):
                return True
        return False


    def scrap(self,page,writer):
        print("_")
        for a in page.find_all(class_="offers_item"):
            item = [0 for _ in range(3)]
            x = a.find_all(class_="offers_item_link_cnt_part")
            if x[0] and self.check_tags(x[0].text):
                item[0] = x[0].text.strip()
                item[2] = x[1].text.strip()
                x = a.find(class_="offers_item_desc_loc")
                if x:
                    item[1] = x.text.strip()
                writer.writerow(item)
            
        print("Done processing page ")
    def load_data(self):
        #Otwieranie pliku csv
        f = open('./data/pracuj.csv', 'w+',newline='')
        writer = csv.writer(f)
        print("Loading data...")
        executor = ThreadPoolExecutor(8)
        pages = []
        oferty = []
        page = 1
        does_next_exist = True
        while page<3000 and does_next_exist:
            print(f'Pobieranie strony {page}')
            with urllib.request.urlopen(urllib.request.Request(self.url(2022,1,page),headers=hdr)) as resp:
                print(f'Parsowanie strony {page}')
                processed_page = BeautifulSoup(resp.read().decode('utf-8'), "html.parser")
                future = executor.submit(self.scrap, (processed_page),writer)
                future.result()
                if(processed_page.find(class_="offers_nav_next") == None):
                    does_next_exist=False
            page+=1
        f.close()
        
if __name__ ==  "__main__":
    loader = Loader()
    loader.load_data()