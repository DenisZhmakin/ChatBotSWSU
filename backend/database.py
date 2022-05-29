import functools

from sqlalchemy import create_engine, MetaData, Table


def singleton(cls):
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if not wrapper.instance:
            wrapper.instance = cls(*args, **kwargs)
        return wrapper.instance

    wrapper.instance = None
    return wrapper


@singleton
class Database:
    def __init__(self):
        self.engine = create_engine('sqlite:////home/denis/Projects/Python/ChatBotSWSU/main.db')
        self.engine.connect()

        self.acronyms = None
        self.subcategories = None
        self.categories = None
        self.idioms = None
        self.post_init()

    def post_init(self):
        import sqlalchemy
        metadata = MetaData()

        if sqlalchemy.inspect(self.engine).has_table("Categories"):
            self.categories = Table('Categories', metadata, autoload_with=self.engine)

        if sqlalchemy.inspect(self.engine).has_table("Subcategories"):
            self.subcategories = Table('Subcategories', metadata, autoload_with=self.engine)

        if sqlalchemy.inspect(self.engine).has_table("Acronyms"):
            self.acronyms = Table('Acronyms', metadata, autoload_with=self.engine)

        if sqlalchemy.inspect(self.engine).has_table("Idioms"):
            self.idioms = Table('Idioms', metadata, autoload_with=self.engine)
