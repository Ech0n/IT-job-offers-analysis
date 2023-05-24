import json
import re
import pandas as pd
import urllib
import urllib.request
from bs4 import BeautifulSoup

url = "https://archiwum.pracuj.pl/archive/offers?Year=2023&Month=1&PageNumber="

def url(rok,miesiac,strona):
    return str(f'https://archiwum.pracuj.pl/archive/offers?Year={rok}&Month={miesiac}&PageNumber={strona}')
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

tagi = ["software","programmer","programista"]

def check_tags(title):
    for wyraz in title.split():
        if( wyraz.lower() in tagi):
            return True
    return False


pages = []
def scrap(page):
    print("_")
    for a in page.find_all(class_="offers_item"):
        x = a.find(class_="offers_item_link_cnt_part")
        if x and check_tags(x.text):
            print(x.text)
            

oferty = []
page = 1
while page<3000:
    print(f'Pobieranie strony {page}')
    with urllib.request.urlopen(urllib.request.Request(url(2022,1,page),headers=hdr)) as resp:
        print(f'Parsowanie strony {page}')
        processed_page = BeautifulSoup(resp.read().decode('utf-8'), "html.parser")
        print(f'Przetwarzanie strony {page}')
        scrap(processed_page)
        if(processed_page.find(class_="offers_nav_next") == None):
            break
    page+=1
