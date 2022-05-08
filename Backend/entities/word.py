from dataclasses import dataclass


@dataclass
class Word:
    text: str
    lang: str
    speech_parts: list[str]
    translation: str

