class BookServiceExceptions:
    AUTHOR_NULL_OR_EMPTY = "Author cannot be null or empty"
    TITLE_NULL_OR_EMPTY = "Title cannot be null or empty"
    PUBLICATION_YEAR_NULL_OR_EMPTY = "Publication year cannot be null or empty"
    BOOK_ALREADY_TAKEN = "This book is already taken"
    BOOK_ALREADY_IN_LIBRARY = "This book is already in the library"
    BOOK_ID_NOT_EXIST = "Book with such id doesn't exist"
    PUBLICATION_YEAR_NOT_INTEGER = "Publication year must be an integer"