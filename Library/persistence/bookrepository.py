import os
import json
import uuid
from Library.persistence.ibookrepository import IBookRepository
from Library.persistence.repositoryexception import RepositoryException
from Library.persistenceentities.bookentity import BookEntity

class BookRepository(IBookRepository):
    def __init__(self, file_path: str):
        self.__file_path = file_path

    def create_book(self, book: BookEntity):
        try:
            existing_books = []
            if os.path.exists(self.__file_path):
                existing_books = self.read_books() or []

            book.id = str(uuid.uuid4())
            existing_books.append(book)

            with open(self.__file_path, 'w') as file:
                json.dump([book.to_dict() for book in existing_books], file, indent=2)
            
            return book
        except Exception as e:
            raise RepositoryException(f"Error creating book: {e}")

    def read_books(self):
        try:
            if os.path.exists(self.__file_path):
                with open(self.__file_path, 'r') as file:
                    books_list = json.load(file)
                    return [BookEntity.from_dict(book_dict) for book_dict in books_list]
            else:
                return []

        except FileNotFoundError:
            raise RepositoryException(f"File of books not found.")
        except Exception as e:
            raise RepositoryException(f"Error reading file: {e}")

    def update_book(self, updated_book: BookEntity):
        try:
            existing_books = self.read_books() or []

            for book in existing_books:
                if book.id == updated_book.id:
                    book.title = updated_book.title
                    book.author = updated_book.author
                    book.publication_year = updated_book.publication_year
                    book.is_taken = updated_book.is_taken

            with open(self.__file_path, 'w') as file:
                json.dump([book.to_dict() for book in existing_books], file, indent=2)

            return updated_book
        except Exception as e:
            raise RepositoryException(f"Error updating book: {e}")
