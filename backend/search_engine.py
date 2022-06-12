import cld3
import requests
from googletrans import Translator
from sqlalchemy import and_

from backend.database import Database
from backend.entities.word import Word
from backend.literals.lang import Language


class SearchEngine:
    def __init__(self):
        self.translator = Translator()
        self.db = Database()

    @staticmethod
    def lang_detect(text: str) -> Language:
        detector = cld3.get_language(text)
        return Language(detector.language)

    def find_idiom(self, idiom_text: str):
        from sqlalchemy import select

        idioms = self.db.idioms
        conn = self.db.engine.connect()

        result = conn.execute(select([idioms]).where(
            idioms.c.phrase == idiom_text
        )).fetchone()

        if result is not None:
            return self.get_translate(result.explanation)

        return "Идиома не найдена"

    def find_abbreviations(self, abbr_text: str):
        from sqlalchemy import select

        acronyms = self.db.acronyms
        subcategories = self.db.subcategories
        conn = self.db.engine.connect()

        abbreviations = conn.execute(select([
            acronyms.c.reduction,
            acronyms.c.transcript,
            subcategories.c.name
        ]).select_from(
            acronyms.join(subcategories)
        ).where(
            acronyms.c.reduction == abbr_text
        ).limit(10)).fetchall()

        if abbreviations is not None:
            result = ""
            # ('API', 'Academic Perofrmance Index', 'Academic & Science')
            for elem in abbreviations:
                result += f"Расшифровка: {self.translator.translate(elem[1], dest='ru').text}\n" + \
                          f"Категория: {self.translator.translate(elem[2], dest='ru').text}\n"
            return result

        return "Аббревиатура не найдена"

    @staticmethod
    def get_word_info(word: str):
        response = requests.get(
            'https://dictionary.yandex.net/dicservice.json/lookupMultiple',
            params={
                'ui': 'ru',
                'srv': 'tr-text',
                'text': word,
                'type': 'regular,syn,ant,deriv',
                'lang': 'en-ru',
                'flags': '15783',
                'dict': 'en-ru.regular,en.syn,en.ant,en.deriv',
            },
            headers={
                'Accept': '*/*',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                'Origin': 'https://translate.yandex.ru',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Referer': 'https://translate.yandex.ru/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
            }
        ).json()

        return Word.from_json(response)

    def get_translate(self, text: str):
        source = SearchEngine.lang_detect(text)

        if source.value == "ru":
            return self.translator.translate(text, dest='en').text
        elif source.value == "en":
            return self.translator.translate(text, dest='ru').text
        else:
            return f"Поддержка данного языка ({source.value}) не реализована"
