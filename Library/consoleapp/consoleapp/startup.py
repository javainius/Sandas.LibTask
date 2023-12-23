from Library.consoleapp.consoleapp.application import Application
from Library.consoleapp.consoleapp.configuration import get_configuration
from Library.persistence.persistence.bookrepository import BookRepository
from Library.services.services.bookservice import BookService

applictaion = Application()
data = get_configuration()

book_file_path = data['connection']['book_file_path']
book_service = BookService(BookRepository(book_file_path))

applictaion.setup(book_service)
applictaion.run()

