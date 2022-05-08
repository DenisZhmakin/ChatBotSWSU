from dataclasses import dataclass


@dataclass
class Phrase:
    match: str
    rus_synonym: str
    eng_synonym: str
