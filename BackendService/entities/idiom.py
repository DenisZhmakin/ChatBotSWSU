from dataclasses import dataclass


@dataclass
class Idiom:
    text: str
    lang: str
    translation: str
    context: str

    @classmethod
    def from_json(cls, json: str):
        pass

    def to_json(self):
        pass
