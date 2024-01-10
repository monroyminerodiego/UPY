'''
Yahoo Finanzas: https://es-us.finanzas.yahoo.com/screener/new/
'''


import os; os.system('cls')
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'

option = webdriver.ChromeOptions()
# options.add_argument('--start-maximized' )

driver = webdriver.Chrome(driver_path,options=option)