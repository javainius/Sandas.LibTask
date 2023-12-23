class BookModel:
    def __init__(self, title, author, publication_year, id = None, is_taken = False):
        self.__title = title
        self.__author = author
        self.__publication_year = publication_year
        self.__id = id
        self.__is_taken = is_taken

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, new_title):
        self.__title = new_title

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, new_author):
        self.__author = new_author

    @property
    def publication_year(self):
        return self.__publication_year

    @publication_year.setter
    def publication_year(self, new_publication_date):
        self.__publication_year = new_publication_date

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, new_id):
        self.__id = new_id

    @property
    def is_taken(self):
        return self.__is_taken

    @is_taken.setter
    def is_taken(self, is_taken):
        self.__is_taken = is_taken