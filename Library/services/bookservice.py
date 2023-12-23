import datetime
from Library.persistence.ibookrepository import IBookRepository
from Library.persistenceentities.bookentity import BookEntity
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
        
        self._check_publication_year_type(book.publication_year)
        
        new_book = self.__book_repository.create_book(bookmodel_to_bookentity(book))
        book_model = bookentity_to_bookmodel(new_book)

        return book_model

    def buy_book_copy(self, book_id, publication_year):
        book = self._get_book(book_id)

        if book is None:
            raise ValueError("Book with such id doesn't exist")
        
        if self._is_null_or_empty(publication_year):
            publication_year = datetime.datetime.now().year
        else:
            self._check_publication_year_type(publication_year)

        book.publication_year = publication_year
        return self.create_book(book)
        

    def get_all_books(self):
        books = self.__book_repository.read_books()
        return  [bookentity_to_bookmodel(book) for book in books]
    
    def take_book(self, book_id):
        pass

    def return_book(self, book_id):
        pass

    def find_book(self, title = None, author = None):
        pass

    def _is_null_or_empty(self, value: str):
        return value is None or value == ""
    
    def _get_book(self, book_id):
        existing_books = self.get_all_books()

        for book in existing_books:
            if book.id == book_id:
                return book

        return None
    
    def _check_publication_year_type(self, year):
            if not isinstance(year, int):
                raise ValueError("PublicationYear must be a number")