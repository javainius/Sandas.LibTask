import datetime
from Library.persistence.ibookrepository import IBookRepository
from Library.persistenceentities.bookentity import BookEntity
from Library.services.bookvalueexception import BookValueException
from Library.services.ibookservice import IBookService
from Library.services.mappers import bookentity_to_bookmodel, bookmodel_to_bookentity
from Library.servicesmodels.bookmodel import BookModel


class BookService(IBookService):
    def __init__(self, book_repository: IBookRepository):
        self.__book_repository = book_repository

    def create_book(self, book: BookModel):
        if self._is_null_or_empty(book.author):
            raise ValueError("Author cannot be null or empty")
        
        if self._is_null_or_empty(book.title):
            raise ValueError("Title cannot be null or empty")

        if self._is_null_or_empty(book.publication_year):
            raise ValueError("Publication year cannot be null or empty")
        
        book.publication_year = self._change_publication_year_type(book.publication_year)
        
        new_book = self.__book_repository.create_book(bookmodel_to_bookentity(book))
        book_model = bookentity_to_bookmodel(new_book)

        return book_model

    def buy_book_copy(self, book_id, publication_year):
        book = self._get_book(book_id)
        
        if self._is_null_or_empty(publication_year):
            publication_year = datetime.datetime.now().year
        else:
            publication_year = self._change_publication_year_type(publication_year)

        book.publication_year = publication_year
        return self.create_book(book)
        

    def get_all_books(self):
        books = self.__book_repository.read_books()
        return  [bookentity_to_bookmodel(book) for book in books]
    
    def take_book(self, book_id):
        book = self._get_book(book_id)
        if book.is_taken:
            raise BookValueException("This book is already taken")

        book.is_taken = True
        
        return self.__book_repository.update_book(book)
        
    def return_book(self, book_id):
        book = self._get_book(book_id)
        if not book.is_taken:
            raise BookValueException("This book is already in the library")

        book.is_taken = False
        
        return self.__book_repository.update_book(book)

    def find_book(self, title = None, author = None):
        pass

    def _is_null_or_empty(self, value: str):
        return value is None or value == ""
    
    def _get_book(self, book_id):
        existing_books = self.get_all_books()

        for book in existing_books:
            if book.id == book_id:
                return book
            
        raise ValueError("Book with such id doesn't exist")
        
    
    def _change_publication_year_type(self, year):
            try:
                return int(year)
            except ValueError:
                raise ValueError("Publication year must be a number")
                