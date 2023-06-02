import json
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import numpy as np
import threading
import atexit
import asyncio
import aiohttp

#old user-agent
#Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11
tagi = np.loadtxt("./config/search_tags.txt",dtype=str)
hdr = {'User-Agent': 'scraper_for_university_project_data_will_not_be_published/1.0',
       'Fron':'matid@spoko.pl',
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
        self.auto_save_value = self.conf["auto_save_every_n_pages"]
        # for i in range(2014,2024):
        #     self.stats[str(i)]={}
        #     for j in range(1,13):
        #         self.stats[str(i)][str(j)]={"pages":0,"all_offers":0,"matched_offers":0}
        with open('./config/last_session.json',"r",encoding="utf-8") as f:
            self.last_session = json.load(f)
            if "stats" in self.last_session:
                self.stats = self.last_session["stats"]
                self.last_page = self.last_session["page"]

        self.time_out = 0
        self.chunk_size = self.conf["chunk_size"]

    def open_file(self):
        try:
            out_file = open("./data/"+self.file_name,"r",encoding="utf-8")
            self.load_file(out_file)
            out_file.close()
        except Exception as ex:
            print("Could not open json file: "+self.file_name+";",ex)
            with open("./data/"+self.file_name,"w+",encoding="utf-8") as f:
                f.write("{}")
            self.data = {}
                

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
                self.stats[year][month]["pages"] = page

    def save_progress(self):
        # if 'stats' in self.conf:
        #     staty_stare = self.conf['stats']
        #     for key in staty_stare.keys():
        #         for subkey in key.keys():
        #             self.stats[key][subkey]+=staty_stare[key][subkey]
        
        progress = {
            'page':self.last_page,
            'month':self.last_month,
            'year':self.last_year,
            'stats':self.stats
        }
        with open('./config/last_session.json', 'w+') as file:
            json.dump(progress, file,indent=4)
        with open('./data/'+self.file_name, 'w+', encoding="utf-8") as file:
            json.dump(self.data, file,indent=self.conf["data_indent"],ensure_ascii=False)
        with open('./config/pracuj_attribute_names.txt', 'w+') as file:
            for element in self.tags:
                file.write(str(element) + "\n")
        
    async def load_data_async(self):
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
                    await self.load_all_pages_async(str(month),str(year),page)
                    page = 1
                    month += inc
                    self.save_progress()
                    print("Scraping next month!!")

            else:     
                while month <= 12 and month >0:
                    self.last_month = month
                    print(f"Scraping for month {month}")
                    await self.load_all_pages_async(str(month),str(year),page)
                    month += inc
                    page = 1
                    self.save_progress()

                    print("Scraping next month!!")
            if inc>0:
                month = 0
            else:
                month = 12
            year+=inc
            print("Scraping next year!!")
            
    async def load_all_pages_async(self,month,year,page=1):        
        print("Loading data...")
        chunk = [None for _ in range(self.chunk_size)]
    
        for i in range(self.chunk_size):
            chunk[i] = asyncio.create_task(self.load_page_chunk(page+i,year,month))
        for i in range(self.chunk_size):
            await chunk[i]


    async def get_async(self,url):
        async with aiohttp.ClientSession() as session:
            if self.time_out != 0:
                await asyncio.sleep(self.time_out)
            tries = 1
            while True:
                async with session.get(url,headers=hdr) as response:
                    if response.status == 200:
                        return await response.text()

                    print("                                                     Status code: ",response.status)
                    if response.headers['Retry-After']:
                        delay = int( response.headers['Retry-After'])
                    else:
                        delay= min(tries*tries*self.conf["delay"],self.conf['page_end_delay'])
                    # print(response.headers['Retry-After'])
                    print(f"Requesting again in {delay} seconds...")
                    self.time_out = delay
                    await asyncio.sleep(delay)
                    self.time_out = 0
                    tries += 1
                
    async def load_page_chunk(self,page,year,month):
            print(f'Pobieranie strony {page} m:{month},y:{year}')
            resp = await self.get_async(self.url(year,month,page))
            print(f'Parsowanie strony {page}')
            processed_page = BeautifulSoup(resp, "html.parser")
            retry_amount = 3
            i = 0
            while processed_page.find(class_="offers_empty") and i < retry_amount-1: 
                print("             Checking for page end one more time")
                await asyncio.sleep(self.conf["page_end_delay"])
                resp = await self.get_async(self.url(year,month,page))
                processed_page = BeautifulSoup(resp, "html.parser")
                i+=1
            if(processed_page.find(class_="offers_empty")):
                print("                 page does not exist! ",self.url(year,month,page))
            else:
                await self.scrap_async(processed_page,(year,month,page))
                page+=4
                if (page%self.auto_save_value)==0:
                    self.save_progress()
                self.last_page=page
                self.stats[year][month]["pages"] = page
                next_page = asyncio.create_task(self.load_page_chunk(page,year,month))
                await next_page

    def start(self):
        asyncio.run(self.load_data_async())

    

if __name__ ==  "__main__":
    loader = Loader()
    loader.start()