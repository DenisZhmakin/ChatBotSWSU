from dataclasses import dataclass

from backend.exceptions.lang_exception import LanguageSupportNotImplementedException


@dataclass(frozen=True)
class Language:
    value: str

    # def __post_init__(self):
    #     supported_lang = [
    #         "en", "ru"
    #     ]
    #
    #     if self.value not in supported_lang:
    #         raise LanguageSupportNotImplementedException(self.value)
