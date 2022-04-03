import json
from pathlib import Path


class SearchEngine:
    @staticmethod
    def search(text: str, type_search: str):
        if type_search == "idiom":
            json_string = json.loads(Path('../storage/idioms.json').read_text())

            for idiom in json_string["idioms"]:
                if idiom['text'] == text:
                    return idiom["translation"]

        return None
