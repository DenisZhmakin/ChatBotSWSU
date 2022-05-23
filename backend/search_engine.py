import json

import cld3
from googletrans import Translator
from jsonlines import jsonlines

from backend.literals.lang import Language


class SearchEngine:
    def __init__(self):
        self.translator = Translator()

    @staticmethod
    def lang_detect(text: str) -> Language:
        detector = cld3.get_language(text)
        return Language(detector.language)

    def find_idiom(self, idiom: str):
        with jsonlines.open('./idioms.jsonl') as reader:
            for obj in reader:
                info = json.loads(obj)
                if info['phrase'] == idiom:
                    return self.translator.translate(idiom, dest='en').text

        return "Сининим не найден"

    def get_translate(self, text: str):
        source = SearchEngine.lang_detect(text)

        if source.value == "ru":
            return self.translator.translate(text, dest='en').text
        elif source.value == "en":
            return self.translator.translate(text, dest='ru').text
        else:
            return f"Поддержка данного языка ({source.value}) не реализована"

    # @staticmethod
    # def search(text: str, type_search: str):
    #             if type_search == "idiom":
    #         json_string = json.loads(Path('../storage/idioms.json').read_text())
    #
    #         for idiom in json_string["idioms"]:
    #             if idiom['text'] == text:
    #                 return idiom["translation"]
    #
    #     return None
