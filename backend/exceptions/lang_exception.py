class LanguageSupportNotImplementedException(Exception):
    def __init__(self, lang):
        self.message = f"Поддержка данного языка ({lang}) не реализована"
        super().__init__()
