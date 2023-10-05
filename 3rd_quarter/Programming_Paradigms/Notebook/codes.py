import os, random
class Book:
    '''
    Class created to create an object with the principal properties of a 'Book', such as genre, title, the number of pages and the author.

    Methods:
    - @Book.info(): prints in console the information of the 'Book'
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
    '''
    Class that inherits 'Book' class.

    Methods:
    - @Book.assign_shelve(): Method created to asign a book to their respective shelve
    '''
    def __init__(self, genre=str, title=str, n_pages=int, authors=list, editorial=str):
        super().__init__(genre, title, n_pages, authors, editorial)
        self.shelve = ''

    def assign_shelve(self,shelve=str):
        '''
        Assigns a shelve to the book.

        Inputs: 
            shelve type[str]: Expects the shelve in which the @Book will be stored

        Outputs: Returns nothing, but prints in console the change made
        '''
        self.shelve = shelve
        print(f'"{self.title}" is now in shelve {shelve}')



if __name__ == '__main__':
    '''
    Problem: Create a program that models a library of books using classes with the principles of inheritance, polymorphism, and abstraction.
    Expected Output: The program should allow:
        - Adding books of different types (e.g., fiction and non-fiction) to the library
        - Calculate the total number of pages in the library
        - List the titles of all the books in the library.
    '''
    def describe(book):
        '''
        Prints the minimum information of 'book'

        Inputs:
            - book <class 'Library(Book)'>: Expects an object of the class 'Library'

        Output:
            - Returns nothing, but a print in console
        '''
        book.info()
        print('')

    os.system('cls')
    
    books = [
        ['Sci-Fi','Antiheroes',295,['Iria G. Parente','Selene M. Pascual']],
        ['Sci-Fi','Sueños de Piedra',263,['Iria G. Parente', 'Selene M. Pascual']],
        ['Romance','Sí, si es contigo',348,['Calle','Poche']],
        ['Romance','A dos metros de ti',512,['Rachael Lippincott', 'Miiki Daughtry', 'Tobias Iaconis']]
    ]
    shelves = ['A','B','C','D']

    library_data = []

    print(f'{"*"*15} Uploading data {"*"*15}')
    for index in range(len(books)):
        row = books[index]
        book = Library(genre=row[0],title=row[1],n_pages=row[2],authors=row[3])
        book.editorial = 'El Barco de papel'
        
        book.assign_shelve(shelves[random.randint(0,3)])
        describe(book)

        library_data.append(book)

    print(f'\n{"*"*15} Reading data {"*"*15}\nTitles')
    total_number_of_pages = 0
    for book in library_data:
        total_number_of_pages += book.n_pages
        print(f'\t- {book.title}')
    print(f'\nNumber of pages in library: {total_number_of_pages}')
    
