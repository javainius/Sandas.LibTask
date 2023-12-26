from datetime import datetime
import uuid
import pytest
import copy
from unittest.mock import Mock
from Library.persistence.persistenceentities.bookentity import BookEntity
from Library.services.services.bookvalueexception import BookValueException
from Library.services.services.mappers import bookentity_to_bookmodel, bookmodel_to_bookentity
from Library.services.servicesmodels.bookmodel import BookModel
from Library.services.services.bookservice import BookService
from faker import Faker

from Library.services.servicesmodels.valueerrors import BookServiceExceptions

fake = Faker()

@pytest.fixture
def mock_book_repository():
    return Mock()

@pytest.fixture
def book_service(mock_book_repository):
    return BookService(mock_book_repository)

def test_given_valid_book_when_create_book_book_is_created(book_service, mock_book_repository):
    # Given
    new_book_entity = BookEntity(
        title=fake.word(),
        author=fake.name(),
        publication_year=int(fake.year()),
        id=str(uuid.uuid4()),
        is_taken=False
    )
    book_model = BookModel(new_book_entity.title, new_book_entity.author, new_book_entity.publication_year)
    mock_book_repository.create_book.return_value = bookmodel_to_bookentity(new_book_entity)

    # When
    created_book = book_service.create_book(book_model)

    # Then
    assert mock_book_repository.create_book.called
    assert isinstance(created_book, BookModel)
    assert created_book.title == book_model.title
    assert created_book.author == book_model.author
    assert created_book.publication_year == book_model.publication_year
    assert created_book.publication_year == book_model.publication_year
    assert created_book.publication_year == book_model.publication_year

def test_given_book_without_title_when_create_book_then_raises_value_error(book_service, mock_book_repository):
    # Given
    book_model = BookModel("", fake.name(), fake.year())

    # When/Then
    with pytest.raises(ValueError, match=BookServiceExceptions.BOOK_ALREADY_TAKEN):
        book_service.create_book(book_model)
        
def test_given_book_without_author_when_create_book_then_raises_value_error(book_service, mock_book_repository):
    # Given
    book_model = BookModel(fake.word(), "", fake.year())

    # When/Then
    with pytest.raises(ValueError, match=BookServiceExceptions.AUTHOR_NULL_OR_EMPTY):
        book_service.create_book(book_model)

def test_given_book_without_publication_year_when_create_book_then_raises_value_error(book_service, mock_book_repository):
    # Given
    book_model = BookModel(fake.word(), fake.name(), "")

    # When/Then
    with pytest.raises(ValueError, match=BookServiceExceptions.PUBLICATION_YEAR_NULL_OR_EMPTY):
        book_service.create_book(book_model)

def test_given_book_wrong_type_publication_year_when_create_book_then_raises_value_error(book_service, mock_book_repository):
    # Given
    book_model = BookModel(fake.word(), fake.name(), "text")

    # When/Then
    with pytest.raises(ValueError, match=BookServiceExceptions.PUBLICATION_YEAR_NOT_INTEGER):
        book_service.create_book(book_model)

def test_given_book_id_and_publication_year_when_buy_book_copy_then_book_copy_is_returned(book_service, mock_book_repository):
    # Given
    book_id = str(uuid.uuid4())
    publication_year = 2023

    existing_book = BookModel(fake.word(), fake.name(), 2022, book_id, False)
    mock_book_repository.read_books.return_value = [existing_book]
    book_copy = copy.deepcopy(existing_book)
    book_copy.publication_year = publication_year
    mock_book_repository.create_book.return_value = book_copy

    # When
    purchased_book = book_service.buy_book_copy(book_id, publication_year)

    # Then
    assert mock_book_repository.read_books.called
    assert mock_book_repository.create_book.called

    assert isinstance(purchased_book, BookModel)
    assert purchased_book.title == existing_book.title
    assert purchased_book.author == existing_book.author
    assert purchased_book.publication_year == publication_year
    assert purchased_book.is_taken == False
    
def test_given_book_id_when_buy_book_copy_then_book_copy_is_returned(book_service, mock_book_repository):
    # Given
    book_id = str(uuid.uuid4())

    existing_book = BookModel(fake.word() ,fake.name(), 2022, book_id, False)
    mock_book_repository.read_books.return_value = [existing_book]
    book_copy = copy.deepcopy(existing_book)
    book_copy.publication_year = datetime.now().year
    mock_book_repository.create_book.return_value = book_copy

    # When
    purchased_book = book_service.buy_book_copy(book_id, None)

    # Then
    assert mock_book_repository.read_books.called
    assert mock_book_repository.create_book.called

    assert isinstance(purchased_book, BookModel)
    assert purchased_book.title == book_copy.title
    assert purchased_book.author == book_copy.author
    assert purchased_book.publication_year == book_copy.publication_year
    assert purchased_book.is_taken == False

def test_given_wrong_book_id_when_buy_book_copy_then_raises_value_error(book_service, mock_book_repository):
    # Given
    book_id = str(uuid.uuid4())
    existing_book = Mock()
    mock_book_repository.read_books.return_value = [existing_book]

    # When/Then
    with pytest.raises(ValueError, match=BookServiceExceptions.PUBLICATION_YEAR_NOT_INTEGER):
        book_service.buy_book_copy(book_id, "invalid_year")
    assert not mock_book_repository.read_books.called
    assert not mock_book_repository.create_book.called

def test_given_book_wrong_type_publication_year_when_buy_book_copy_then_raises_value_error(book_service, mock_book_repository):
    # Given
    book_id = str(uuid.uuid4())
    existing_book = Mock()
    mock_book_repository.read_books.return_value = [existing_book]

    # When/Then
    with pytest.raises(BookValueException, match=BookServiceExceptions.BOOK_ID_NOT_EXIST):
        book_service.buy_book_copy(book_id, None)
    assert mock_book_repository.read_books.called
    assert not mock_book_repository.create_book.called

def test_given_books_when_get_all_books_books_are_retrieved(book_service, mock_book_repository):
    # Given
    mock_book_repository.read_books.return_value = [
        Mock(),
        Mock(),
        Mock()
    ]

    # When
    all_books = book_service.get_all_books()

    # Then
    assert mock_book_repository.read_books.called
    assert isinstance(all_books, list)
    assert all(isinstance(book, BookModel) for book in all_books)

def test_given_epmty_book_list_when_get_all_books_empty_list_is_retrieved(book_service, mock_book_repository):
    # Given
    mock_book_repository.read_books.return_value = []

    # When
    all_books = book_service.get_all_books()

    # Then
    assert mock_book_repository.read_books.called
    assert isinstance(all_books, list)

def test_given_book_id_when_take_book_then_book_is_returned(book_service, mock_book_repository):
    # Given
    book_id = str(uuid.uuid4())
    book = Mock()
    book.id = book_id
    book.is_taken = False
    updated_book = copy.deepcopy(book)
    updated_book.is_taken = True
    mock_book_repository.read_books.return_value = [book]
    mock_book_repository.update_book.return_value = updated_book

    # When
    taken_book = book_service.take_book(book_id)

    # Then
    assert mock_book_repository.read_books.called
    assert mock_book_repository.update_book.called
    assert taken_book.is_taken is True


def test_given_taken_book_when_take_book_then_raises_bookvalueexception(book_service, mock_book_repository):
    # Given
    book_id = str(uuid.uuid4())
    mock_existing_book = Mock()
    mock_existing_book.is_taken = True
    mock_existing_book.id = book_id
    mock_book_repository.read_books.return_value = [mock_existing_book]

    # When/Then
    with pytest.raises(BookValueException, match=BookServiceExceptions.BOOK_ALREADY_TAKEN):
        book_service.take_book(book_id)
    assert not mock_book_repository.update_book.called

def test_given_nonexistent_book_when_take_book_then_raises_bookvalueexception(book_service, mock_book_repository):
    # Given
    book_id = str(uuid.uuid4())
    mock_book_repository.read_books.return_value = [
        Mock(),
        Mock(),
        Mock()
    ]

    # When/Then
    with pytest.raises(BookValueException, match=BookServiceExceptions.BOOK_ID_NOT_EXIST):
        book_service.take_book(book_id)
    assert not mock_book_repository.update_book.called

def test_given_taken_book_id_when_return_book_then_updated_book_is_returned(book_service, mock_book_repository):
    # Given
    book_id = str(uuid.uuid4())
    taken_book = BookEntity(fake.word(), fake.name(), 2022, book_id, True)
    updated_book = copy.deepcopy(taken_book)
    updated_book.is_taken = False
    mock_book_repository.read_books.return_value = [taken_book]
    mock_book_repository.update_book.return_value = updated_book

    # When
    returned_book = book_service.return_book(book_id)

    # Then  
    assert mock_book_repository.update_book.called
    assert mock_book_repository.read_books.called
    assert returned_book.is_taken is False

def test_given_available_book_id_when_return_book_then_raises_bookvalueexception(book_service, mock_book_repository):
    # Given
    available_book = Mock()
    available_book.is_taken = False
    mock_book_repository.read_books.return_value = [available_book]

    # When, Then
    with pytest.raises(BookValueException, match=BookServiceExceptions.BOOK_ALREADY_IN_LIBRARY):
        book_service.return_book(available_book.id)
    assert mock_book_repository.read_books.called
    assert not mock_book_repository.update_book.called

def test_given_nonexistent_book_id_when_return_book_then_raises_bookvalueexception(book_service, mock_book_repository):
    # Given
    nonexistent_book_id = str(uuid.uuid4())
    mock_book_repository.read_books.return_value = [Mock()]

    # When, Then
    with pytest.raises(BookValueException, match=BookServiceExceptions.BOOK_ID_NOT_EXIST):
        book_service.return_book(nonexistent_book_id)
    assert mock_book_repository.read_books.called
    assert not mock_book_repository.update_book.called


def test_given_matching_title_when_search_books_by_title_then_matching_book_is_returned(book_service, mock_book_repository):
    # Given
    title_to_search = fake.word()
    book_with_matching_title = Mock()
    book_with_matching_title.title = title_to_search
    mock_book_repository.read_books.return_value = [book_with_matching_title]

    # When
    found_books = book_service.search_books_by_title(title_to_search)

    # Then
    assert mock_book_repository.read_books.called
    assert len(found_books) == 1
    assert found_books[0].title == title_to_search

def test_given_nonmatching_title_when_search_books_by_title_then_returned_empty_list(book_service, mock_book_repository):
    # Given
    title_to_search = fake.word()
    book_with_nonmatching_title = Mock()
    mock_book_repository.read_books.return_value = [book_with_nonmatching_title]

    # When
    found_books = book_service.search_books_by_title(title_to_search)

    # Then
    assert mock_book_repository.read_books.called
    assert len(found_books) == 0

def test_given_matching_title_when_search_books_by_title_then_matching_book_is_returned(book_service, mock_book_repository):
    # Given
    title_to_search = fake.word()
    book_with_matching_title = Mock()
    book_with_matching_title.title = title_to_search
    mock_book_repository.read_books.return_value = [book_with_matching_title]

    # When
    found_books = book_service.search_books_by_title(title_to_search)

    # Then
    assert mock_book_repository.read_books.called
    assert len(found_books) == 1
    assert found_books[0].title == title_to_search

def test_given_uprocessed_book_list_when_search_books_by_title_then_returned_filtered_and_sorted_list_returned(book_service, mock_book_repository):
    # Given
    title_to_search = fake.word()
    book_with_matching_title = BookModel(title_to_search, fake.name(), 2000, uuid.uuid4())
    different_publication_year_book = copy.deepcopy(book_with_matching_title)
    different_publication_year_book2 = copy.deepcopy(book_with_matching_title)

    different_publication_year_book.publication_year = 2001
    different_publication_year_book2.publication_year = 2002
    unprocessed_book_list = [
        bookmodel_to_bookentity(different_publication_year_book2),
        bookmodel_to_bookentity(book_with_matching_title),
        bookmodel_to_bookentity(different_publication_year_book),
        bookmodel_to_bookentity(copy.deepcopy(book_with_matching_title)),
        bookmodel_to_bookentity(copy.deepcopy(book_with_matching_title)),
        bookmodel_to_bookentity(copy.deepcopy(book_with_matching_title))
    ]
    mock_book_repository.read_books.return_value = unprocessed_book_list

    expected_book_list = [
        book_with_matching_title,
        different_publication_year_book,
        different_publication_year_book2
    ]

    # When
    found_books = book_service.search_books_by_title(title_to_search)

    # Then
    assert mock_book_repository.read_books.called
    assert found_books == expected_book_list

def test_given_matching_title_when_search_books_by_author_then_matching_book_is_returned(book_service, mock_book_repository):
    # Given
    author_to_search = fake.name()
    book_with_matching_author = Mock()
    book_with_matching_author.title = author_to_search
    mock_book_repository.read_books.return_value = [book_with_matching_author]

    # When
    found_books = book_service.search_books_by_author(author_to_search)

    # Then
    assert mock_book_repository.read_books.called
    assert len(found_books) == 1
    assert found_books[0].title == author_to_search

def test_given_nonmatching_title_when_search_books_by_author_then_returned_empty_list(book_service, mock_book_repository):
    # Given
    author_to_search = fake.word()
    book_with_nonmatching_author = Mock()
    mock_book_repository.read_books.return_value = [book_with_nonmatching_author]

    # When
    found_books = book_service.search_books_by_author(author_to_search)

    # Then
    assert mock_book_repository.read_books.called
    assert len(found_books) == 0

def test_given_matching_title_when_search_books_by_author_then_matching_book_is_returned(book_service, mock_book_repository):
    # Given
    author_to_search = fake.name()
    book_with_matching_author = Mock()
    book_with_matching_author.author = author_to_search
    mock_book_repository.read_books.return_value = [book_with_matching_author]

    # When
    found_books = book_service.search_books_by_author(author_to_search)

    # Then
    assert mock_book_repository.read_books.called
    assert len(found_books) == 1
    assert found_books[0].author == author_to_search

def test_given_uprocessed_book_list_when_search_books_by_author_then_returned_filtered_and_sorted_list_returned(book_service, mock_book_repository):
    # Given
    author_to_search = fake.name()
    book_with_matching_author = BookModel(fake.word(), author_to_search, 2000, uuid.uuid4())
    different_publication_year_book = copy.deepcopy(book_with_matching_author)
    different_publication_year_book2 = copy.deepcopy(book_with_matching_author)

    different_publication_year_book.publication_year = 2001
    different_publication_year_book2.publication_year = 2002
    unprocessed_book_list = [
        bookmodel_to_bookentity(different_publication_year_book2),
        bookmodel_to_bookentity(book_with_matching_author),
        bookmodel_to_bookentity(different_publication_year_book),
        bookmodel_to_bookentity(copy.deepcopy(book_with_matching_author)),
        bookmodel_to_bookentity(copy.deepcopy(book_with_matching_author)),
        bookmodel_to_bookentity(copy.deepcopy(book_with_matching_author))
    ]
    mock_book_repository.read_books.return_value = unprocessed_book_list

    expected_book_list = [
        book_with_matching_author,
        different_publication_year_book,
        different_publication_year_book2
    ]

    # When
    found_books = book_service.search_books_by_author(author_to_search)

    # Then
    assert mock_book_repository.read_books.called
    assert found_books == expected_book_list

if __name__ == "__main__":
    pytest.main()
