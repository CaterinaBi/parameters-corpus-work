from pyrsistent import s
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import time
from time import sleep
from datetime import date, datetime

import nltk
from nltk.tokenize import sent_tokenize

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

        self.dictionaries_list = [] # all dictionaries, will be split into centuries later
        # self.text_links = []

        self.list_1500 = []
        self.list_1600 = []
        self.list_1700 = []
        self.list_1800 = []
        self.list_1900 = []

        print('\n---Program initialised.')

    def create_dictionary(self):
        '''A method that acts like a crawler and creates a dictionary of text metrics and links'''
        value = int

        for number in range(1,3): # change to range 1,501 when scraping all texts

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
                # self.text_links.append(link) # appends link to links list
                self.dictionaries_list.append(dictionary) # only appends dictionary if link is present
                print('Dictionary appended')
            except:
                dictionary['Link'] = 'unavailable'
                print('Dictionary not appended')
                print(dictionary)
                print('\n')
                continue # only appends dictionary if link is present

            print(dictionary)
            print('\n')
            time.sleep(2)

    def extract_text_from_links(self):
        "Method that extracts text from links and appends text to dedicated dictionary key"
        for dictionary in self.dictionaries_list:
            link = dictionary['Link']
            
            self.driver.get(link)
            text = self.driver.find_element(By.CSS_SELECTOR, value="body>pre").text # string

            # text cleaning
            text_list = list(text)
            for character in range(len(text_list)):
                if text_list[character] == '.':
                    text_list[character] = '. '
                elif text_list[character] == '!':
                    text_list[character] = '.! '
                elif text_list[character] == '?':
                    text_list[character] = '? '

            text = "".join(text_list)

            dictionary['Text'] = text
            # print(text)
            time.sleep(2)

        # print(self.dictionaries_list)

    def extract_questions_from_text(self):
        """A method that extracts only interrogatives from scraped texts"""

        for dictionary in self.dictionaries_list:
            interrogatives = []
            text = dictionary['Text']
            sentences = sent_tokenize(text) # list

            for sentence in sentences:
                if '?' in sentence:
                    interrogatives.append(sentence)
                    # append to dict here
                else:
                    continue

            print(interrogatives)

    def create_year_lists(self):
        '''A method that creates lists of dictionaries based on year'''
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

        print(len(list_1500))
        print(len(list_1600))
        print(len(list_1700))
        print(len(list_1800))
        print(len(list_1900))