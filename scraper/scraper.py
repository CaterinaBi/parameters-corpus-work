from pyrsistent import s
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

        print('\n---Program initialised.')