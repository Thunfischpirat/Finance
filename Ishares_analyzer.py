# -*- coding: utf-8 -*-
"""
IShares_analyzer is supposed to help in analyzing a BlackRock iShare Etf.
"""

import requests
import pandas as pd
import bs4 as bs
import urllib.request
import urllib3
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import os.path
link = "https://www.ishares.com/de/professionelle-anleger/de/produkte/284219/fund/1478358465952.ajax?fileType=csv&fileName=2B76_holdings&dataType=fund"

def create_etf(link):
    etf_name = link.split("&")
    etf_name = etf_name[-2].replace("fileName=","")
    if os.path.isfile('Etfs/{}.csv'.format(etf_name)):
         print("Etf already exists!\n")
         etf = pd.read_csv("Etfs/{}.csv".format(etf_name),header = 2)
    else:
        print("Creating new Etf...\n")
        resp = requests.get(link, allow_redirects = True)
        with open('Etfs/{}.csv'.format(etf_name), 'wb') as outfile:
            outfile.write(resp.content)   
        etf = pd.read_csv("Etfs/{}.csv".format(etf_name),header = 2)
    
    return etf
        
def create_descriptions(etf):        
    
    for ISIN in etf.ISIN.values:
        idx_ISIN = list(etf.ISIN.values).index(ISIN)
        name = etf.Name.values[idx_ISIN]
        if os.path.isfile('Etfs/Descriptions/{}_description.txt'.format(name)):
            print("{}_description already exists!\n".format(name))
        else:
            try:
                browser = webdriver.Chrome()  
                browser.get('https://finance.yahoo.com')
                time.sleep(1) 
                accept_button = browser.find_element_by_xpath('//*[@id="consent-page"]/div/div/div/div[3]/div/form/button[1]')
                accept_button.click()
                time.sleep(1)
                searchbox = browser.find_element_by_xpath('//*[@id="yfin-usr-qry"]')
                searchbox.send_keys(ISIN)
                time.sleep(5)
                searchbox.send_keys(Keys.RETURN)
                time.sleep(1)
                url = browser.current_url
                browser.quit()
                url = url.replace("?p","/profile?p")
                source = urllib.request.urlopen(url).read()   
                soup = bs.BeautifulSoup(source,'lxml')
                with open('Etfs/Descriptions/{}_description.txt'.format(name), 'wb') as outfile:
                    for paragraph in soup.find_all('p')[1:]:
                        outfile.write((paragraph.text+"\n").encode("utf-8"))                  
                    print('{}_description.txt created'.format(name))
                
            except urllib.error.HTTPError:
                print("{} not found on Yahoo Finance.\n".format(ISIN))
                pass
            
            except urllib3.exceptions.ProtocolError:
                print("Let's wait a moment...\n")
                time.sleep(20)
                pass
    print("\nDone!")
def get_description(self,name):
    
    with open('Etfs/Descriptions/{}_description.txt'.format(name),"r",encoding='utf8') as description:
        for line in description:
            print(line)
            
    return "\nDone."
    

    
        
    
   
    




