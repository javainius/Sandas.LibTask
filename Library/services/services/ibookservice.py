from abc import ABC, abstractmethod
from Library.services.servicesmodels.bookmodel import BookModel


class IBookService(ABC):
    @abstractmethod
    def create_book(self, book: BookModel):
        pass

    @abstractmethod
    def buy_book_copy(self, book_id, publication_year):
        pass

    @abstractmethod
    def get_all_books(self):
        pass

    @abstractmethod
    def take_book(self, book_id):
        pass

    @abstractmethod
    def return_book(self, book_id):
        pass

    @abstractmethod
    def search_books_by_title(self, title):
        pass

    @abstractmethod
    def search_books_by_author(self, author):
        pass