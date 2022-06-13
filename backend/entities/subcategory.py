# import json
# from pathlib import Path
#
# import requests
# from bs4 import BeautifulSoup
# from sqlalchemy import select
#
# from database import Database
# from .acronym import Acronym
#
# SITE_URL = "https://www.abbreviations.com"
#
#
# class Subcategory:
#     def __init__(self, name: str, link: str, category_name: str, db: Database):
#         self.name = name
#         self.category_name = category_name
#         self.link = link
#         self.db = db
#
#     def get_acronyms_iter(self):
#         page = self.get_page_number()
#
#         while True:
#             resource = requests.get(f"{self.link}/{page}")
#             soap = BeautifulSoup(resource.text, 'html.parser')
#
#             tbody = soap.select_one("div.tdata-ext.col-sm-12").table.tbody
#
#             if tbody is not None:
#                 for tr_elem in tbody.children:
#                     yield Acronym(
#                         reduction=tr_elem.select_one("td.tal.tm.fsl").a.text,
#                         transcript=tr_elem.select_one("td.tal.dm.fsl").text,
#                         subcategory_name=self.name,
#                         db=self.db
#                     )
#                 page += 1
#                 self.set_page_number(page)
#             else:
#                 break
#
#     def get_page_number(self):
#         subcategories = self.db.subcategories
#         conn = self.db.engine.connect()
#
#         return conn.execute(select([subcategories]).where(
#             subcategories.c.name == self.name
#         )).fetchone().page
#
#     def set_page_number(self, page_number):
#         from sqlalchemy import update
#
#         subcategories = self.db.subcategories
#         conn = self.db.engine.connect()
#
#         conn.execute(
#             update(subcategories).where(
#                 subcategories.c.name == self.name
#             ).values(
#                 page=page_number
#             )
#         )
#
#     def check_existence(self):
#         subcategories = self.db.subcategories
#         select_subcategories = select(subcategories).where(
#             subcategories.c.name == self.name
#         )
#
#         conn = self.db.engine.connect()
#         if conn.execute(select_subcategories).fetchall():
#             return True
#
#         return False
#
#     def check_completeness(self):
#         subcategories = self.db.subcategories
#         conn = self.db.engine.connect()
#
#         result = conn.execute(select([subcategories]).where(
#             subcategories.c.name == self.name
#         )).fetchone()
#
#         return result.completeness
#
#     def write(self):
#         categories = self.db.categories
#         subcategories = self.db.subcategories
#         conn = self.db.engine.connect()
#
#         conn.execute(
#             subcategories.insert().values(
#                 name=self.name,
#                 page=1,
#                 category_id=conn.execute(select([categories]).where(
#                     categories.c.name == self.category_name
#                 )).fetchone().id
#             )
#         )
#
#     def complete(self):
#         from sqlalchemy import update
#
#         subcategories = self.db.subcategories
#         conn = self.db.engine.connect()
#
#         conn.execute(
#             update(subcategories).where(
#                 subcategories.c.name == self.name
#             ).values(
#                 completeness=True
#             )
#         )
