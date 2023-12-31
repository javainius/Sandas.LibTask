class BookContract:
    def __init__(self, title, author, publication_year, id = None, is_taken = False):
        self._title = title
        self._author = author
        self._publication_year = publication_year
        self._id = id
        self._is_taken = is_taken

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        self._title = new_title

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, new_author):
        self._author = new_author

    @property
    def publication_year(self):
        return self._publication_year

    @publication_year.setter
    def publication_year(self, new_publication_date):
        self._publication_year = new_publication_date

    @property
    def book_id(self):
        return self._id

    @book_id.setter
    def book_id(self, new_id):
        self._id = new_id

    @property
    def is_taken(self):
        return self._is_taken

    @is_taken.setter
    def is_taken(self, is_taken):
        self._is_taken = is_taken