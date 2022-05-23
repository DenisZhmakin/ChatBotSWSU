# from sqlalchemy import create_engine, MetaData, Table, Column, Text, Integer, ForeignKey, Boolean
#
#
# class Database:
#     def __init__(self):
#         self.acronyms = None
#         self.subcategories = None
#         self.categories = None
#         self.engine = create_engine('sqlite:///abbreviations.db')
#         self.engine.connect()
#
#     def create_table_categories(self):
#         metadata = MetaData()
#
#         self.categories = Table('Categories', metadata,
#                                 Column('id', Integer, primary_key=True),
#                                 Column('completeness', Boolean, default=False),
#                                 Column('name', Text),
#                                 sqlite_autoincrement=True
#                                 )
#
#         metadata.create_all(self.engine)
#
#     def create_table_subcategories(self):
#         metadata = MetaData()
#
#         self.subcategories = Table('Subcategories', metadata,
#                                    Column('id', Integer, primary_key=True),
#                                    Column('name', Text),
#                                    Column('category_id', Integer, ForeignKey(self.categories.c.id)),
#                                    Column('completeness', Boolean, default=False),
#                                    Column('page', Integer, default=1),
#                                    sqlite_autoincrement=True
#                                    )
#
#         metadata.create_all(self.engine)
#
#     def create_table_acronyms(self):
#         metadata = MetaData()
#
#         self.acronyms = Table('Acronyms', metadata,
#                               Column('id', Integer, primary_key=True),
#                               Column('reduction', Text),
#                               Column('transcript', Text),
#                               Column('subcategory_id', Integer, ForeignKey(self.subcategories.c.id)),
#                               sqlite_autoincrement=True
#                               )
#
#         metadata.create_all(self.engine)
#
#     def post_init(self):
#         import sqlalchemy
#         metadata = MetaData()
#
#         if sqlalchemy.inspect(self.engine).has_table("Categories"):
#             self.categories = Table('Categories', metadata, autoload_with=self.engine)
#         else:
#             self.create_table_categories()
#
#         if sqlalchemy.inspect(self.engine).has_table("Subcategories"):
#             self.subcategories = Table('Subcategories', metadata, autoload_with=self.engine)
#         else:
#             self.create_table_subcategories()
#
#         if sqlalchemy.inspect(self.engine).has_table("Acronyms"):
#             self.acronyms = Table('Acronyms', metadata, autoload_with=self.engine)
#         else:
#             self.create_table_acronyms()
