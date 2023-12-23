from Library.consoleapp.mappers import bookcontract_to_bookmodel, bookmodel_to_bookcontract
from Library.consoleappcontracts.bookcontract import BookContract
from Library.persistence.repositoryexception import RepositoryException
from Library.services.ibookservice import IBookService

class Application:
    def setup(self, book_service: IBookService):
        self.__book_service = book_service
    
    def run(self):
        while True:
            print("choose an action which want you want to do: ")

            print("1 -> create a book")
            print("2 -> buy a book copy and add to the library")
            print("3 -> take a book from the library")
            print("4 -> return a book to the library")
            print("5 -> search for a book by a title or an author")

            action = input("write your action: ").lower()
            action_functions = self._action_functions()

            selected_action = action_functions.get(action, self._invalid_action)
            selected_action()

    def _action_functions(self):
        return {
            "1": self._create_book,
            "2": self._buy_book_copy,
            "3": self._take_book,
            "4": self._return_book,
            "5": self._search_for_book,
        }
    
    def _create_book(self):
        
        print("Book creation:")
        book_title = input("Enter title: ")
        book_author = input("Enter author: ")
        book_publication_year = input("Enter publication_year: ")

        new_book = BookContract(book_title, book_author, book_publication_year)

        try:
            created_book = self.__book_service.create_book(bookcontract_to_bookmodel(new_book))
            bookcontract = bookmodel_to_bookcontract(created_book)

            print("Created book:")
            self._print_book(bookcontract)

        except ValueError as e:
            print(f"Value error occured: {e}")
        except RepositoryException as e:
            print(f"Repository exception occured: {e}")

    def _buy_book_copy(self):
        print("Which book copy you want to buy?")

        try:
            existing_books = self.__book_service.get_all_books()
            existing_books = [bookmodel_to_bookcontract(book) for book in existing_books]
            
            for book in existing_books:
                self._print_book(book)

            book_id = input("Enter the id of the book you want to buy a copy of:")
            book_publication_year = input("Enter the publication year, if you won't enter it, then publication "
                                          + "year will be the current year ")
            new_book_copy = bookmodel_to_bookcontract(self.__book_service.buy_book_copy(book_id, book_publication_year))

            print("New book copy:")
            self._print_book(new_book_copy)

        except ValueError as e:
            print(f"Value error occured: {e}")
        except RepositoryException as e:
            print(f"Repository exception occured: {e}")

    def _print_book(self, book):
        print(f"Book id: {book.book_id}")
        print(f"Book title: {book.title}")
        print(f"Book author: {book.author}")
        print(f"Book publication year: {book.publication_year}")
        print(f"Is book taken: {book.is_taken}")

    def _take_book(self):
        print("Taking a book from the library")

    def _return_book(self):
        print("Returning a book to the library")

    def _search_for_book(self):
        print("Searching for a book by title or author")

    def _invalid_action(self):
        print("Invalid action. Please choose a valid option.")