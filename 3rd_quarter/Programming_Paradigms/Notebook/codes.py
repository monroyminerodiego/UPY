import os
class Book:
    '''
    Class created to create an object with the principal properties of a 'Book', such as genre, title, the number of pages and the author.

    Methods:
    - .info(): prints in console the information of the 'Book'
    '''
    def __init__(self,genre=str,title=str, n_pages=int, authors=list, editorial=str):
        self.title = title
        self.n_pages = n_pages
        self.authors = authors
        self.genre = genre
        self.editorial = editorial

    def info(self):
        '''
        Prints a message with the information of the 'Book'

        Inputs: Expects no inputs/arguments

        Outputs: Returns nothing, but prints in console the infomation of the book
        '''
        print(f"Genre: {self.genre}\nTitle: '{self.title}'\nNo. of Pages: '{self.n_pages}'\nAuthors: {self.authors}\nEditorial: {self.editorial}")

class Library(Book):
    def __init__(self, genre=str, title=str, n_pages=int, authors=list, editorial=str):
        super().__init__(genre, title, n_pages, authors, editorial)
        self.shelve = ''

    def assign_shelve(self,shelve=str):
        self.shelve = shelve
        print(f'{self.title} is now in shelve {shelve}')



if __name__ == '__main__':
    '''
    Problem: Create a program that models a library of books using classes with the principles of inheritance, polymorphism, and abstraction.
    Expected Output: The program should allow:
        - Adding books of different types (e.g., fiction and non-fiction) to the library
        - Calculate the total number of pages in the library
        - List the titles of all the books in the library.
    '''
    os.system('cls')
    
    books = [
        ['Sci-Fi','Antiheroes',295,['Iria G. Parente','Selene M. Pascual']],
        ['Sci-Fi','Sueños de Piedra',263,['Iria G. Parente', 'Selene M. Pascual']],
        ['Romance','Sí, si es contigo',348,['Calle','Poche']],
        ['Romance','A dos metros de ti',512,['Rachael Lippincott', 'Miiki Daughtry', 'Tobias Iaconis']]
    ]
    shelves = ['A','B','C','D']

    for index in range(len(books)):
        row = books[index]
        book = Library(genre=row[0],title=row[1],n_pages=row[2],authors=row[3])
        book.info()
        print("*"*15)

        book.editorial = 'El Barco de papel'
        book.assign_shelve(shelves[index])