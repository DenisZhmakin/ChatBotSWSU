# import json
# from pathlib import Path
#
# import requests
# from bs4 import BeautifulSoup
# from sqlalchemy import select, insert
#
# from .subcategory import Subcategory
#
# SITE_URL = "https://www.abbreviations.com"
#
#
# class Category:
#     def __init__(self, name: str, link: str):
#         self.name = name
#         self.link = link
#
#     def get_subcategories_iter(self):
#         resource = requests.get(self.link)
#         soap = BeautifulSoup(resource.text, 'lxml')
#         tbody = soap.select_one("div.tdata-ext.col-sm-12").table.tbody
#
#         for tr_elem in tbody.children:
#             yield Subcategory(
#                 name=tr_elem.select_one("td.tal.vam.sc").a.text,
#                 link=f'{SITE_URL}{tr_elem.select_one("td.tal.vam.sc").a["href"]}',
#                 category_name=self.name, db=self.db
#             )
#
#     def check_existence(self):
#         categories = self.db.categories
#         select_categories = select([categories]).where(
#             categories.c.name == self.name
#         )
#
#         conn = self.db.engine.connect()
#         if conn.execute(select_categories).fetchall():
#             return True
#
#         return False
#
#     def check_completeness(self):
#         categories = self.db.categories
#         conn = self.db.engine.connect()
#
#         result = conn.execute(select([categories]).where(
#             categories.c.name == self.name
#         )).fetchone()
#
#         return result.completeness
#
#     def write(self):
#         categories = self.db.categories
#         conn = self.db.engine.connect()
#
#         conn.execute(
#             categories.insert().values(
#                 name=self.name
#             )
#         )
#
#     def complete(self):
#         from sqlalchemy import update
#
#         categories = self.db.categories
#         conn = self.db.engine.connect()
#
#         conn.execute(
#             update(categories).where(
#                 categories.c.name == self.name
#             ).values(
#                 completeness=True
#             )
#         )
