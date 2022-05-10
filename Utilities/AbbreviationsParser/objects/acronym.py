from pathlib import Path


class Acronym:
    def __init__(self, reduction, transcript, link, subcategory_name):
        self.reduction = reduction
        self.subcategory_name = subcategory_name

        self.manifest = Path('../../..') / 'storage' / 'abbreviations' / \
            'acronyms' / self.subcategory_name / 'manifest.json'

        self.transcript = transcript
        self.link = link
