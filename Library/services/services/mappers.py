from Library.persistence.persistenceentities.bookentity import BookEntity
from Library.services.servicesmodels.bookmodel import BookModel


def bookmodel_to_bookentity(book: BookModel):
    return BookEntity(book.title, book.author, book.publication_year, book.id, book.is_taken)

def bookentity_to_bookmodel(book: BookEntity) -> BookModel:
    return BookModel(book.title, book.author, book.publication_year, book.id, book.is_taken)