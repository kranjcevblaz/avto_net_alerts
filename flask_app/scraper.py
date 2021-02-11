#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 19:41:44 2021

@author: blazkranjcev
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from datetime import date
from datetime import timedelta
import re
import pandas as pd
import numpy as np
import os
import smtplib
from email.message import EmailMessage
import myEnvVal

# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

server_path = True
if server_path:
    exec_path = "/home/blazkranjcev97/avto_net_alerts/flask_app/chromedriver"
else:
    exec_path = "/Users/blazkranjcev/python_excercises/avto_net_scraper/flask_app/chromedriver"

chrome_options = webdriver.ChromeOptions()
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_options, executable_path=exec_path)

try:
    driver.get("https://www.google.com")
    print(f'Page title was {driver.title}')

finally:
    driver.quit()
    
def get_brands():
    driver = webdriver.Chrome('/Users/blazkranjcev/python_excercises/avto_net_scraper/chromedriver')
    url = "https://www.avto.net/"
    driver.get(url)
    
    brands = []
    selectBrand = Select(driver.find_element_by_id('make'))
    
    for option in selectBrand.options:
        d = option.text
        brands.append((d,d))
        
    driver.close()
    
    brands = list(dict.fromkeys(brands))
    return brands
    

def get_dropdown_model_options(brand):
    driver = webdriver.Chrome('/Users/blazkranjcev/python_excercises/avto_net_scraper/chromedriver')
    url = "https://www.avto.net/"
    driver.get(url)
    
    model_options = []
    selectBrand = Select(driver.find_element_by_id('make'))
    selectBrand.select_by_value(brand)
    selectModel = Select(driver.find_element_by_id('model'))
    
    for option in selectModel.options:
        d = option.text
        model_options.append((d,d))
        

    model_options.remove(('Vsi modeli', 'Vsi modeli'))
        
    driver.close()
    return model_options

def run_scraper(brand, model, price_min='0', price_max='999999', year_min='0', year_max='2090', km_max='9999999', fuel='vsa goriva'):
    fuel_type_dict = {'vsa goriva': '0', 'bencin': '201', 'diesel': '202', 'plin': '203', 'hibridni pogon': '205', 'e-pogon': '207'}
    # driver = webdriver.Chrome('/Users/blazkranjcev/python_excercises/avto_net_scraper/chromedriver')
    search_by_string = '4x4'

    url_first = "https://www.avto.net/Ads/results.asp?znamka={brand}&model={model}&modelID=&tip=katerikoli%20tip&znamka2=&model2=&tip2=katerikoli%20tip&znamka3=&model3=&tip3=katerikoli%20tip&cenaMin={price_min}&cenaMax={price_max}&letnikMin={year_min}&letnikMax={year_max}&bencin={fuel}&starost2=999&oblika=0&ccmMin=0&ccmMax=99999&mocMin=&mocMax=&kmMin=0&kmMax={km_max}&kwMin=0&kwMax=999&motortakt=0&motorvalji=0&lokacija=0&sirina=0&dolzina=&dolzinaMIN=0&dolzinaMAX=100&nosilnostMIN=0&nosilnostMAX=999999&lezisc=&presek=0&premer=0&col=0&vijakov=0&EToznaka=0&vozilo=&airbag=&barva=&barvaint=&EQ1=1000000000&EQ2=1000000000&EQ3=1000000000&EQ4=100000000&EQ5=1000000000&EQ6=1000000000&EQ7=1110100120&EQ8=1010000001&EQ9=1000000000&KAT=1010000000&PIA=&PIAzero=&PSLO=&akcija=0&paketgarancije=&broker=0&prikazkategorije=0&kategorija=0&ONLvid=0&ONLnak=0&zaloga=10&arhiv=0&presort=3&tipsort=DESC&stran=1"
    url = "https://www.avto.net/Ads/results.asp?znamka={brand}&model={model}&modelID=&tip=katerikoli%20tip&znamka2=&model2=&tip2=katerikoli%20tip&znamka3=&model3=&tip3=katerikoli%20tip&cenaMin={price_min}&cenaMax={price_max}&letnikMin={year_min}&letnikMax={year_max}&bencin={fuel}&starost2=999&oblika=0&ccmMin=0&ccmMax=99999&mocMin=&mocMax=&kmMin=0&kmMax={km_max}&kwMin=0&kwMax=999&motortakt=0&motorvalji=0&lokacija=0&sirina=0&dolzina=&dolzinaMIN=0&dolzinaMAX=100&nosilnostMIN=0&nosilnostMAX=999999&lezisc=&presek=0&premer=0&col=0&vijakov=0&EToznaka=0&vozilo=&airbag=&barva=&barvaint=&EQ1=1000000000&EQ2=1000000000&EQ3=1000000000&EQ4=100000000&EQ5=1000000000&EQ6=1000000000&EQ7=1110100120&EQ8=1010000001&EQ9=1000000000&KAT=1010000000&PIA=&PIAzero=&PSLO=&akcija=0&paketgarancije=&broker=0&prikazkategorije=0&kategorija=0&ONLvid=0&ONLnak=0&zaloga=10&arhiv=0&presort=3&tipsort=DESC&stran={pg}"
    driver.get(url_first.format(brand=brand, model=model, price_min=price_min, price_max=price_max, year_min=year_min, year_max=year_max, km_max=km_max, fuel=fuel_type_dict[fuel]))
    
    source = driver.page_source
    sel_soup = BeautifulSoup(source, 'html.parser')
    
    pages = sel_soup.find_all('a', {'class': 'page-link'})
    pages_text_list = [x.text for x in pages]
    pages_cleaner = ['Nazaj', 'Naprej', '\n\nNazaj\n', '\nNaprej\n\n', '\n\n']
    pages_cleaned = [x for x in pages_text_list if x not in pages_cleaner]
    pages_cleaned = list(set(pages_cleaned))
    pages_cleaned = [int(i) for i in pages_cleaned]
    pages_cleaned.sort()
    
    data_names = [] 
    data_prices = [] 
    data_url = []
    data = []
    for pg in pages_cleaned:
        print(pg)
        driver.get(url.format(brand=brand, model=model, price_min=price_min, price_max=price_max, year_min=year_min, year_max=year_max, km_max=km_max, fuel=fuel_type_dict[fuel], pg=pg))
        source = driver.page_source
        sel_soup = BeautifulSoup(source, 'html.parser')
        car_elements = sel_soup.find_all('table', {'class': 'table table-striped table-sm table-borderless font-weight-normal mb-0'})
        car_names = sel_soup.find_all('div', {'class': 'GO-Results-Naziv bg-dark px-3 py-2 font-weight-bold text-truncate text-white text-decoration-none'})
        car_prices = sel_soup.find_all('div', {'class': 'GO-Results-Price-TXT-Regular'})
        car_urls = sel_soup.find_all('div', {'class': 'row bg-white position-relative GO-Results-Row GO-Shadow-B'})
        
        for element in car_names:
            name = element.find_all('span')
            inner_text_car_name = [x.text for x in name]
            
            data_names.append(inner_text_car_name)
            
        for element in car_prices:
            price = element.text
            
            data_prices.append(price)
        
        for element in car_urls:
            car_url = element.find('a')['href']
            
            data_url.append(car_url)
        
        for element in car_elements:
            rows = element.find_all('td')
            inner_text_list = [x.text for x in rows]
            
            if len(inner_text_list) < 10:
                inner_text_list.insert(2, 'None')
                
        
            data.append(inner_text_list)
        
    data = [[x.replace('\n','') for x in l] for l in data]
    headers = ['1.registracija', 'Prevoženih', 'Gorivo', 'Menjalnik', 'Motor', 'Naziv', 'Cena', 'URL']
    drop_list_strings = ['Starost', '1.registracija', 'Prevoženih', 'Gorivo', 'Menjalnik', 'Motor']
    data_cleaned = [[x for x in group if x not in drop_list_strings] for group in data]
    
    for x, y in zip(data_cleaned, data_names):
        x.append(y)
        
    for x, y in zip(data_cleaned, data_prices):
        x.append(y)
        
    for x, y in zip(data_cleaned, data_url):
        x.append(y)
    
    df = pd.DataFrame(data_cleaned, columns=headers)
    
    # dataframe string transforms
    df['Prevoženih'] = df['Prevoženih'].replace(['None'], np.nan)
    df['Prevoženih'] = df['Prevoženih'].str.split(' ').str[0]
    df['Prevoženih'] = df['Prevoženih'].astype(float)
    
    def split_name(name): 
        split_name = name.split(',') 
        return split_name if len(split_name) == 2 else [np.nan, split_name[0]]
    
    def split_power(name): 
        split_name = name.split('/') 
        return split_name if len(split_name) == 2 else [split_name[0], np.nan]
    
    motor_df = pd.DataFrame(df.Motor.apply(split_name).tolist(), columns=['Prostornina', 'Moč'])
    concat_list = [df,motor_df]
    df = pd.concat(concat_list, axis=1)
    
    df['Prostornina'] = df['Prostornina'].str.split(' ccm').str[0]
    df['Prostornina'] = df['Prostornina'].astype(float)
    
    power_df = pd.DataFrame(df.Moč.apply(split_power).tolist(), columns=['kW', 'KM'])
    concat_list = [df,power_df]
    df = pd.concat(concat_list, axis=1)
    
    df['kW'] = df['kW'].str.split(' kW').str[0]
    df['kW'] = df['kW'].astype(float)
    df['KM'] = df['KM'].str.split(' KM').str[0]
    df['KM'] = df['KM'].astype(float)
    
    df['Naziv'] = df['Naziv'].str.get(0)
    
    df['Cena'] = df['Cena'].str.split(' €').str[0]
    df['Cena'] = df['Cena'].replace(['Pokličite za ceno!'], np.nan)
    df['Cena'] = df['Cena'].str.replace('.', '', regex=False)
    df['Cena'] = df['Cena'].astype(float)
    
    df.drop(columns=['Moč', 'Motor'], inplace=True)
    
    # unique ID based on URL
    unique_id_list = []
    url_name_list = []
    for row in range(len(df['URL'])):
        unique_id = re.findall(r'=(\w+)', df['URL'][row])[0]
        unique_name = df['URL'][row].rsplit('=',2)[2:][0]
        unique_id_list.append(unique_id)
        url_name_list.append(unique_name)
    
    df['URL'] = df['URL'].str.replace('..', 'https://www.avto.net', regex=False)
    df['Unique_ID'] = unique_id_list
    df['Unique_ID'] = df['Unique_ID'].astype(float)
    df['Unique_URL_Name'] = url_name_list
    
    today = date.today()
    yesterday = today - timedelta(days=1)
    d_today = today.strftime('%d%m%Y')
    d_yesterday = yesterday.strftime('%d%m%Y')
    
    today_csv_file_name = str(brand + '_' + model + '_' + d_today + '.csv')
    yesterday_csv_file_name = str(brand + '_' + model + '_' + d_yesterday + '.csv')
    
    df.to_csv(today_csv_file_name, encoding='utf-8', index=False)
    
    try:
        yesterday_df = pd.read_csv(yesterday_csv_file_name)
        new_cars = df[~df['Unique_ID'].isin(yesterday_df['Unique_ID'])]
    except:
        print('Prvi dan obvestil')
    
    df_string = df[df['Naziv'].str.contains(search_by_string)]

    driver.close()
    
    return {'brand': brand, 'model': model, 'new_cars': new_cars}

def send_email(brand, model, new_cars, email_address):
    EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    
    # call object EmailMessage and assign categories to it
    msg = EmailMessage()
    msg['Subject'] = 'Novi oglasi za {0} {1}'.format(brand, model)
    msg['From'] = email_address
    msg['To'] = email_address
    
    msg.set_content('Novi oglasi za vozilo {0} {1}'.format(brand, model))
    msg.add_alternative('''
                        {}
                        '''.format(new_cars.to_html()), subtype='html')
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:    
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        smtp.send_message(msg)
        
def main_func(brand, model, price_min, price_max, year_min, year_max, km_max, fuel, email_address):
    myEnvVal.setVar()
    scraper_data = run_scraper(brand, model, price_min, price_max, year_min, year_max, km_max, fuel)
    send_email(scraper_data['brand'], scraper_data['model'], scraper_data['new_cars'], email_address)
    