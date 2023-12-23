from Library.consoleapp.application import Application
from Library.consoleapp.configuration import get_configuration
from Library.persistence.bookrepository import BookRepository
from Library.services.bookservice import BookService

applictaion = Application()
data = get_configuration()

book_file_path = data['connection']['book_file_path']
book_service = BookService(BookRepository(book_file_path))

applictaion.setup(book_service)
applictaion.run()

