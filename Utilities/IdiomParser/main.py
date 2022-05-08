import json
import re
import string

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.native-english.ru"
IDIOMS_PART = "idioms/category"


def _main():
    obj = {
        "idioms": [

        ]
    }
    for letter in string.ascii_lowercase:
        page_number = 1
        while True:
            response = requests.get(f"{BASE_URL}/{IDIOMS_PART}/{letter}/{page_number}")

            soup = BeautifulSoup(response.text, 'lxml')

            for idiom in soup.find_all("a", {"class": ["pane__link", "jsl"]}):
                response_idiom = requests.get(f"{BASE_URL}/{idiom['href']}")
                soup = BeautifulSoup(response_idiom.text, 'lxml')

                temp = re.sub(r'\([^)]*\)', "?", soup.find("h1", {"class": "title"}).span.text)
                text = " ".join([word for word in temp.split() if word != "?"])
                translate = soup.find("div", {"class": "article"}).p.text

                print(text)

                obj["idioms"].append({
                    "text": text,
                    "lang": "en-US",
                    "translation": translate,
                    "context": "common"
                })

            next_page = soup.find("a", {"class": "pager__item_next"})

            if next_page is not None:
                page_number = next_page['href'].split('/')[-1]
            else:
                break

    with open('../../Storage/idioms.json', 'w', encoding='utf-8') as file:
        json.dump(obj, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    _main()
