from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class Word:
    speech_part: str
    translates: List[str] = field(default_factory=list)
    synonyms: List[str] = field(default_factory=list)
    antonyms: List[str] = field(default_factory=list)
    related_words: List[str] = field(default_factory=list)

    @staticmethod
    def get_related_words(related_words_list: list):
        antonyms = list()

        if related_words_list:
            for top_block in related_words_list[0]['tr']:
                antonyms.append(top_block['text'])

                if 'syn' not in top_block:
                    break

                for sub_block in top_block['syn']:
                    antonyms.append(sub_block['text'])

        return antonyms

    @staticmethod
    def get_antonyms(ant_list: list):
        antonyms = list()

        if ant_list:
            for top_block in ant_list[0]['tr']:
                antonyms.append(top_block['text'])

                if 'syn' not in top_block:
                    break

                for sub_block in top_block['syn']:
                    antonyms.append(sub_block['text'])

        return antonyms

    @staticmethod
    def get_synonyms(syn_list: list):
        synonyms = list()

        if syn_list:
            for top_block in syn_list[0]['tr']:
                synonyms.append(top_block['text'])

                if 'syn' not in top_block:
                    break

                for sub_block in top_block['syn']:
                    synonyms.append(sub_block['text'])

        return synonyms

    @staticmethod
    def get_translates(translate_list: list):
        synonyms = list()

        if translate_list:
            for top_block in translate_list[0]['tr']:
                synonyms.append(top_block['text'])

                if 'syn' not in top_block:
                    break

                for sub_block in top_block['syn']:
                    synonyms.append(sub_block['text'])

        return synonyms

    @classmethod
    def from_json(cls, json: dict):
        if 'code' not in json:
            return cls(
                speech_part=json['en-ru']['regular'][0]['pos']['tooltip'] if json['en-ru']['regular'] else "",
                translates=Word.get_translates(json['en-ru']['regular']),
                synonyms=Word.get_synonyms(json['en']['syn']),
                antonyms=Word.get_antonyms(json['en']['ant']),
                related_words=Word.get_related_words(json['en']['deriv'])
            )
