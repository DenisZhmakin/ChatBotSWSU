from dataclasses import dataclass
from typing import Optional


@dataclass
class Word:
    type: str
    morph: Optional[list[str]]
    rus_synonym: str
    eng_synonym: str
