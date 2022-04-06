import json

import requests
from bs4 import BeautifulSoup

BASE_SITE_URL = "https://wooordhunt.ru"
EN_RU_DICT = "/dic/content/en_ru"


def _main():
    response = requests.get(f"{BASE_SITE_URL}{EN_RU_DICT}")
    soup = BeautifulSoup(response.text, 'lxml')

    for a in soup.find_all('a', href=True):
        if "/dic/list/en_ru" in a['href']:
            response_inner = requests.get(f"{BASE_SITE_URL}{a['href']}")
            soup_inner = BeautifulSoup(response_inner.text, 'lxml')

            for a_inner in soup_inner.find_all('a', href=True):
                if "/word" in a_inner['href']:
                    word_response = requests.get(f"{BASE_SITE_URL}{a_inner['href']}")
                    word_soup = BeautifulSoup(word_response.text, 'lxml')

                    word_text = ""
                    word_translate = ""
                    speech_parts = []

                    try:
                        raw_text = word_soup.find("div", {"id": "wd_title"}).h1
                        if raw_text is not None:
                            if raw_text.find('span'):
                                root = BeautifulSoup(str(raw_text), 'lxml')
                                h1 = root.select_one('h1')
                                h1.select_one('span').decompose()
                                word_text = h1.text.strip()
                            else:
                                word_text = raw_text.text.strip()
                    except AttributeError:
                        continue

                    raw_translate = word_soup.find("div", {"class": "t_inline_en"})
                    if raw_translate is not None:
                        word_translate = raw_translate.text.strip()

                    for part in word_soup.find_all("h4", {"class": "pos_item"}):
                        if "↓" in part.text:
                            speech_parts.append(part.text.replace("↓", ""))
                        else:
                            speech_parts.append(part.text)

                    with open('../../storage/english_words.json', 'r+', encoding='utf-8') as file:
                        words = json.load(file)
                        file.seek(0)
                        words["english_words"].append({
                            "text": word_text.lower(),
                            "lang": "en-US",
                            "speech_parts": speech_parts,
                            "translation": word_translate
                        })

                        json.dump(words, file, indent=4, ensure_ascii=False)

                    print(word_text.lower())


if __name__ == '__main__':
    _main()
