import os
import requests
import asyncio
from bs4 import BeautifulSoup

class main:
    # =============== CONSTRUCTOR ===============
    def __init__(self,word:str, verbose:bool = False):
        '''
        '''
        self.word    = word
        self.url     = f"https://listado.mercadolibre.com.mx/{word}#result"
        self.verbose = verbose

    # =============== PRIVATE METHODS ===============
    def __get_html(self):
        '''
        '''
        r = requests.get(self.url)
        if r.status_code == 200:
            return [True,r.text]
        return [False,'No code 200']

    def __get_results(self,soup:BeautifulSoup):
        '''
        '''
        resultados = soup.find_all('span',{'class':'ui-search-search-result__quantity-results'})
        print(resultados)

    def __get_categories(self,soup:BeautifulSoup):
        '''
        '''
        section_container = soup.find('section')
        sections = section_container.find_all('div',{'class':'ui-search-filter-dl'})
        categories = sections[4]
        list_categories = categories.find('ul')

        for categorie in list_categories:
            print(categorie.get_text())
        

    # =============== PUBLIC METHODS ===============
    def start(self):
        '''
        '''
        self.inform(f"The word to check is {self.word}...")

        html_code = self.__get_html()
        if not(html_code[0]): return # Validar que pasa si no se en cuentra URL

        soup = BeautifulSoup(html_code[1],'lxml')

        self.__get_results(soup)

        self.__get_categories(soup)


        
    def inform(self,message:str):
        '''
        Informs the user about a message related to the Spyder bot's operation.

        ### Args:
        * `message` (str): The message to be conveyed.
        '''
        if self.verbose: print(message)





if __name__ == '__main__':
    os.system('cls')

    from faker import Faker

    fake = Faker()

    test = main(
        word    = fake.word(),
        verbose = True
    )

    test.start()