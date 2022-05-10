import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

from Utilities.AbbreviationsParser.objects.category import Category

SITE_URL = "https://www.abbreviations.com"


def save_acronyms(subcategory: dict):
    print(subcategory['link'])
    page = 1

    category_name = subcategory['parent']['name'].replace(' ', '')
    subcategory_name = sanitize_filename(subcategory['name'].replace(' ', ''))

    folder = Path('./acronyms') / sanitize_filename(category_name)
    folder.mkdir(parents=True, exist_ok=True)
    filename = folder / f"{subcategory_name}.jsonl"
    filename.touch()

    while True:
        resource = requests.get(f"{subcategory['link']}/{page}")
        soap = BeautifulSoup(resource.text, 'html.parser')

        tbody = soap.select_one("div.tdata-ext.col-sm-12").table.tbody

        if tbody is not None:
            page = page + 1
        else:
            break

        for tr_elem in tbody.children:
            href = tr_elem.select_one("td.tal.tm.fsl").a['href']
            reduction = tr_elem.select_one("td.tal.tm.fsl").a.text
            transcript = tr_elem.select_one("td.tal.dm.fsl").text

            acronym = {
                "reduction": reduction,
                "link": f"{SITE_URL}{href}",
                "parent": subcategory_name,
                "transcript": transcript
            }

            with open(str(filename), 'a') as file:
                file.write(json.dumps(acronym))
                file.write('\n')

        print(f"Page = {page}")


def save_subcategories(category: dict):
    resource = requests.get(category['link'])
    soap = BeautifulSoup(resource.text, 'html.parser')

    tbody = soap.select_one("div.tdata-ext.col-sm-12").table.tbody

    folder = Path('./subcategories')
    folder.mkdir(parents=True, exist_ok=True)
    filename = folder / f"{sanitize_filename(category['name'].replace(' ', ''))}.jsonl"

    for tr_elem in tbody.children:
        href = tr_elem.select_one("td.tal.vam.sc").a["href"]
        name = tr_elem.select_one("td.tal.vam.sc").a.text
        count = tr_elem.select_one("td.tar.vam.cn").text

        subcategory = {
            "name": name,
            "parent": category,
            "link": f"{SITE_URL}{href}",
            "count": count
        }

        save_acronyms(subcategory)
        print(filename)

        with open(str(filename), 'a') as file:
            file.write(json.dumps(subcategory))
            file.write('\n')


def _main():
    resource = requests.get(SITE_URL)
    soap = BeautifulSoup(resource.text, 'html.parser')

    ctree = soap.find(id="ctree")

    for div in ctree.select("div.col-xs-12.col-sm-6"):
        category = Category(
            name=div.header.a.text,
            link=f"{SITE_URL}{div.header.a['href']}"
        )

        if category.check_existence():
            continue

        for subcategory in category.get_subcategories_iter():
            # save_subcategories(vars(category))
            pass

        category.save()


if __name__ == '__main__':
    _main()
