from pyrsistent import s
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import time
from time import sleep
from datetime import date, datetime

import json
import os
import requests
import uuid

class Scraper:
    def __init__(self, url: str = 'https://www.theatre-classique.fr/pages/programmes/PageEdition.php'):
        '''
        This class is used to scrape a website and extract text from it.
        '''
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.get(url) # look for all properties for sale within a 10-mile radius from Cambridge, UK
        time.sleep(2)

        self.id_number = 0

        print('\n---Program initialised.')

    def create_dictionary(self):
        '''A method that acts like a crawler and creates a dictionary of text metrics and links'''
        value = int

        list_1500 = []
        list_1600 = []
        list_1700 = []
        list_1800 = []
        list_1900 = []

        for number in range(1,501):

            dictionary = {}

            value = number
            table_row = f"#table_AA>tbody>tr:nth-child({value})"
            author_row = f"#table_AA>tbody>tr:nth-child({value})>td:nth-child(1)>a"
            title_row = f"#table_AA>tbody>tr:nth-child({value})>td:nth-child(2)"
            date_row = f"#table_AA>tbody>tr:nth-child({value})>td:nth-child(3)>a"
            genre_row = f"#table_AA>tbody>tr:nth-child({value})>td:nth-child(4)"
            text_row= f"#table_AA>tbody>tr:nth-child({value})>td:nth-child(8)>a"

            contents = self.driver.find_element(By.CSS_SELECTOR, value="#table_AA>tbody")
            row = contents.find_element(By.CSS_SELECTOR, value=table_row)

            # id generator
            self.id_number += 1 
            text_id = f'text_{self.id_number}'
            dictionary['ID'] = text_id

            # contents to scrape
            author = row.find_element(By.CSS_SELECTOR, value=author_row).text
            dictionary['Author'] = author
            title = row.find_element(By.CSS_SELECTOR, value=title_row).text
            dictionary['Title'] = title

            try:
                date = int(row.find_element(By.CSS_SELECTOR, value=date_row).text)
                dictionary['Date'] = date
            except:
                dictionary['Date'] = 1500

            genre = row.find_element(By.CSS_SELECTOR, value=genre_row).text
            dictionary['Genre'] = genre
            
            try:
                text = row.find_element(By.CSS_SELECTOR, value=text_row)
                link = text.get_attribute('href')
                dictionary['Link'] = link
            except:
                dictionary['Link'] = 'unavailable'

            match1500 = r'^(15)([0-9]{2})$'
            match1600 = r'^(16)([0-9]{2})$'
            match1700 = r'^(17)([0-9]{2})$'
            match1800 = r'^(18)([0-9]{2})$'
            match1900 = r'^(19)([0-9]{2})$'

            if re.match(match1500, str(date)):
                print('String goes in 1500 dictionary')
                list_1500.append(dictionary)
                print(list_1500)
            elif re.match(match1600, str(date)):
                print('String goes in 1600 dictionary')
                list_1600.append(dictionary)
                print(list_1600)
            elif re.match(match1700, str(date)):
                print('String goes in 1700 dictionary')
                list_1700.append(dictionary)
                print(list_1700)
            elif re.match(match1800, str(date)):
                print('String goes in 1800 dictionary')
                list_1800.append(dictionary)
                print(list_1800)
            elif re.match(match1900, str(date)):
                print('String goes in 1900 dictionary')
                list_1900.append(dictionary)
                print(list_1900)

            # print(dictionary)
            time.sleep(2)
    
        print(len(list_1500))
        print(len(list_1600))
        print(len(list_1700))
        print(len(list_1800))
        print(len(list_1900))

    def create_global_list(self):
        '''A method that creates a list of links to the properties to scrape'''
        self.whole_query_links.extend(self.all_text_links_list)
        
        return self.whole_query_links