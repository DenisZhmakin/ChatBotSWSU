import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from jsonlines import jsonlines
from pathvalidate import sanitize_filename

from Utilities.AbbreviationsParser.objects.acronym import Acronym

SITE_URL = "https://www.abbreviations.com"


class Subcategory:
    subcategories_files = Path('../../..') / 'storage' / 'abbreviations' / 'subcategories'
    acronymus_folder = Path('../../..') / 'storage' / 'abbreviations' / 'acronyms'

    def __init__(self, name: str, link: str, category_name: str, count: int):
        self.name = name
        self.link = link
        self.category_name = sanitize_filename(category_name.replace(' ', ''))

        self.manifest = Subcategory.acronymus_folder / self.category_name / 'manifest.json'
        self.manifest.touch()

        self.count = 0
        self.page = 1

    def get_acronyms_iter(self):
        while True:
            resource = requests.get(f"{self.link}/{self.page}")
            soap = BeautifulSoup(resource.text, 'html.parser')

            tbody = soap.select_one("div.tdata-ext.col-sm-12").table.tbody

            if tbody is not None:
                for tr_elem in tbody.children:
                    yield Acronym(
                        reduction=tr_elem.select_one("td.tal.tm.fsl").a.text,
                        transcript=tr_elem.select_one("td.tal.dm.fsl").text,
                        link=f'{SITE_URL}{tr_elem.select_one("td.tal.tm.fsl").a["href"]}',
                        subcategory_name=sanitize_filename(self.name.replace(' ', ''))
                    )
                self.set_page_number(self.page)
                self.page += 1
            else:
                break

    def check_existence(self):
        with jsonlines.open(Subcategory.subcategories_files / f"{self.category_name}.jsonl", mode='r') as reader:
            for obj in reader:
                if obj['name'] == self.name:
                    return True

        return False

    def set_page_number(self, page_number: int):
        pass

    def save(self):
        with open(Subcategory.subcategories_files / f"{self.category_name}.jsonl", 'a', encoding='utf-8') as file:
            json.dump(self, file)
            file.write('\n')

    def to_dict(self):
        return vars(self)

# def save_acronyms(subcategory: dict):
#     print(subcategory['link'])
#     page = 1
#
#     category_name = subcategory['parent']['name'].replace(' ', '')
#     subcategory_name = sanitize_filename(subcategory['name'].replace(' ', ''))
#
#     folder = Path('./acronyms') / sanitize_filename(category_name)
#     folder.mkdir(parents=True, exist_ok=True)
#     filename = folder / f"{subcategory_name}.jsonl"
#     filename.touch()
#
#     while True:
#         resource = requests.get(f"{subcategory['link']}/{page}")
#         soap = BeautifulSoup(resource.text, 'html.parser')
#
#         tbody = soap.select_one("div.tdata-ext.col-sm-12").table.tbody
#
#         if tbody is not None:
#             page = page + 1
#         else:
#             break
#
#         for tr_elem in tbody.children:
#             href = tr_elem.select_one("td.tal.tm.fsl").a['href']
#             reduction = tr_elem.select_one("td.tal.tm.fsl").a.text
#             transcript = tr_elem.select_one("td.tal.dm.fsl").text
#
#             acronym = {
#                 "reduction": reduction,
#                 "link": f"{SITE_URL}{href}",
#                 "parent": subcategory_name,
#                 "transcript": transcript
#             }
#
#             with open(str(filename), 'a') as file:
#                 file.write(json.dumps(acronym))
#                 file.write('\n')
#
#         print(f"Page = {page}")
