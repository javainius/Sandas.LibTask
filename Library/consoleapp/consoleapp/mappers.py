from Library.consoleapp.consoleappcontracts.bookcontract import BookContract
from Library.services.servicesmodels.bookmodel import BookModel


def bookcontract_to_bookmodel(book: BookContract):
    return BookModel(book.title, book.author, book.publication_year)

def bookmodel_to_bookcontract(book: BookModel):
    return BookContract(book.title, book.author, book.publication_year, book.id, book.is_taken)