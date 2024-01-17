'''
Yahoo Finanzas: https://es-us.finanzas.yahoo.com/screener/new/
'''


import os; os.system('cls')
import requests
from bs4 import BeautifulSoup

req = requests.get('https://es.aliexpress.com/w/wholesale-celular.html?spm=a2g0o.home.search.0')

print(req)