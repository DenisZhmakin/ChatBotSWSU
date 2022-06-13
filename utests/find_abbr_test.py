from unittest import main
from unittest import TestCase

from backend.search_engine import SearchEngine


class FindAbbrTest(TestCase):
    def setUp(self):
        self.engine = SearchEngine()

    def test_find_valid_abbr(self):
        result = self.engine.find_abbreviations("API")
        self.assertNotEqual(result, "")

    def test_find_abbr_first_capital(self):
        result = self.engine.find_abbreviations("Api")
        self.assertNotEqual(result, "")

    def test_find_abbr_lowercase(self):
        result = self.engine.find_abbreviations("api")
        self.assertNotEqual(result, "")

    def test_find_abbr_mixed_up(self):
        result = self.engine.find_abbreviations("aPi")
        self.assertNotEqual(result, "")

    def test_find_abbr_extra_spaces(self):
        result = self.engine.find_abbreviations("  Api   ")
        self.assertEqual(result, "")

    def test_find_abbr_with_none(self):
        with self.assertRaises(AttributeError):
            self.engine.find_idiom(None)

    def test_find_abbr_with_empty_string(self):
        result = self.engine.find_idiom("")
        self.assertEqual(result, "Идиома не найдена")

    def test_find_abbr_with_passing_digits(self):
        with self.assertRaises(AttributeError):
            self.engine.find_idiom(8888)


if __name__ == "__main__":
    main()
