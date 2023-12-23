from Library.persistenceentities.bookentity import BookEntity
from Library.servicesmodels.bookmodel import BookModel


def bookmodel_to_bookentity(book: BookModel):
    return BookEntity(book.title, book.author, book.publication_year)

def bookentity_to_bookmodel(book: BookEntity):
    book_model = BookModel(book.title, book.author, book.publication_year, book.id, book.is_taken)

    return book_model