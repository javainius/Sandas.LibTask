from abc import ABC, abstractmethod

class IBookRepository(ABC):
    @abstractmethod
    def create_book(self):
        pass
    
    @abstractmethod
    def read_books(self):
        pass

    @abstractmethod
    def update_book(self, updated_book):
        pass