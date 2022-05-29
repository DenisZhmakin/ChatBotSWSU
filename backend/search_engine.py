import cld3
from googletrans import Translator

from backend.database import Database
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

        return "Сининим не найден"

    def find_abbreviations(self, abbr_text: str):
        from sqlalchemy import select

        return self

    def get_translate(self, text: str):
        source = SearchEngine.lang_detect(text)

        if source.value == "ru":
            return self.translator.translate(text, dest='en').text
        elif source.value == "en":
            return self.translator.translate(text, dest='ru').text
        else:
            return f"Поддержка данного языка ({source.value}) не реализована"