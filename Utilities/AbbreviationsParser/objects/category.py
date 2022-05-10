import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from jsonlines import jsonlines

from Utilities.AbbreviationsParser.objects.subcategory import Subcategory

SITE_URL = "https://www.abbreviations.com"


class Category:
    categories_file = Path('../../..') / 'storage' / 'abbreviations' / 'categories.jsonl'

    def __init__(self, name: str, link: str):
        self.name = name
        self.link = link

    def get_subcategories_iter(self):
        resource = requests.get(self.link)
        soap = BeautifulSoup(resource.text, 'lxml')
        tbody = soap.select_one("div.tdata-ext.col-sm-12").table.tbody

        for tr_elem in tbody.children:
            yield Subcategory(
                name=tr_elem.select_one("td.tal.vam.sc").a.text,
                link=f'{SITE_URL}{tr_elem.select_one("td.tal.vam.sc").a["href"]}',
                category_name=self.name,
                count=int(tr_elem.select_one("td.tar.vam.cn").text)
            )

    def check_existence(self):
        with jsonlines.open(Category.categories_file, mode='r') as reader:
            for obj in reader:
                if obj['name'] == self.name:
                    return True

        return False

    def save(self):
        with open(Category.categories_file, 'a', encoding='utf-8') as file:
            json.dump(self, file)
            file.write('\n')

    def to_dict(self):
        return vars(self)
