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
from core import Loader


# url = "https://archiwum.pracuj.pl/archive/offers?Year=2023&Month=1&PageNumber="
# tagi = ["software","programmer","programista"]
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
delay = 5

class Basic_Loader(Loader):
    def __init__(self) -> None:
        self.file_name = "basic.json"
        super().__init__()
        self.out_file_name = './data/pracuj_detailed.csv'
        with open(self.out_file_name, 'w+',newline='', encoding='utf-8') as f:
            f.truncate(0)
    # def open_file(self):
    #     try:
    #         out_file = open("./data/basic.json","r")
    #         self.load_file(out_file)
    #         out_file.close()
    #     except Exception as ex:
    #         print("Could not open json file, ",ex)
    def scrap(self,page,date):
        print("_")
        f = open('./data/pracuj_basic.csv', 'a+',newline='', encoding='utf-8')
        writer = csv.writer(f)
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
        f.close()
        print("Done processing page ")


loader = None
if __name__ ==  "__main__":
    with Basic_Loader() as loader:
        loader.load_data()

