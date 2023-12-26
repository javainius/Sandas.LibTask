from datetime import datetime
from Library.persistence.persistence.ibookrepository import IBookRepository
from Library.services.services.bookvalueexception import BookValueException
from Library.services.services.ibookservice import IBookService
from Library.services.services.mappers import bookentity_to_bookmodel, bookmodel_to_bookentity
from Library.services.servicesmodels.bookmodel import BookModel
from Library.services.servicesmodels.valueerrors import BookServiceExceptions


class BookService(IBookService):
    def __init__(self, book_repository: IBookRepository):
        self._book_repository = book_repository

    def create_book(self, book: BookModel):
        if self._is_null_or_empty(book.author):
            raise ValueError(BookServiceExceptions.AUTHOR_NULL_OR_EMPTY)
        
        if self._is_null_or_empty(book.title):
            raise ValueError(BookServiceExceptions.TITLE_NULL_OR_EMPTY)

        if self._is_null_or_empty(book.publication_year):
            raise ValueError(BookServiceExceptions.PUBLICATION_YEAR_NULL_OR_EMPTY)
        
        book.publication_year = self._change_publication_year_type(book.publication_year)
        
        new_book = self._book_repository.create_book(bookmodel_to_bookentity(book))
        book_model = bookentity_to_bookmodel(new_book)

        return book_model

    def buy_book_copy(self, book_id, publication_year):        
        if self._is_null_or_empty(publication_year):
            publication_year = datetime.now().year
        else:
            publication_year = self._change_publication_year_type(publication_year)

        book = self._get_book(book_id)
        book.publication_year = publication_year
        return self.create_book(book)
        

    def get_all_books(self):
        books = self._book_repository.read_books()
        return  [bookentity_to_bookmodel(book) for book in books]
    
    def take_book(self, book_id):
        book = self._get_book(book_id)
        if book.is_taken:
            raise BookValueException(BookServiceExceptions.BOOK_ALREADY_TAKEN)

        book.is_taken = True
        book = bookmodel_to_bookentity(book)
        
        return bookentity_to_bookmodel(self._book_repository.update_book(book))
        
    def return_book(self, book_id):
        book = self._get_book(book_id)
        if not book.is_taken:
            raise BookValueException(BookServiceExceptions.BOOK_ALREADY_IN_LIBRARY)

        book.is_taken = False
        
        return self._book_repository.update_book(book)

    def search_books_by_title(self, title):
        all_books = self.get_all_books()
        found_books = list(filter(lambda book: book.title == title, all_books))

        return self._filter_books(found_books)
    
    def search_books_by_author(self, author):
        all_books = self.get_all_books()
        found_books = list(filter(lambda book: book.author == author, all_books))

        return self._filter_books(found_books)

    def _filter_books(self, books):
        filtered_books = self._filter_unique_books(books)
        if filtered_books:
            filtered_books.sort(key=lambda book: book.publication_year)
            return filtered_books
        else:
            return []
    
    def _filter_unique_books(self, books):
        unique_books = set()
        filtered_books = []

        for book in books:
            book_key = (book.title, book.author, book.publication_year)

            if book_key not in unique_books:
                unique_books.add(book_key)
                filtered_books.append(book)

        return filtered_books

    def _is_null_or_empty(self, value: str):
        return value is None or value == ""
    
    def _get_book(self, book_id):
        existing_books = self.get_all_books()

        for book in existing_books:
            if book.id == book_id:
                return book
            
        raise BookValueException(BookServiceExceptions.BOOK_ID_NOT_EXIST)
        
    
    def _change_publication_year_type(self, year):
            try:
                return int(year)
            except ValueError:
                raise ValueError(BookServiceExceptions.PUBLICATION_YEAR_NOT_INTEGER)
                