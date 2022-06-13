from unittest import main
from unittest import TestCase

from backend.search_engine import SearchEngine


class FindTestIdiom(TestCase):
    def setUp(self):
        self.engine = SearchEngine()

    def test_find_valid_idiom(self):
        result = self.engine.find_idiom("magic asterisk")
        self.assertEqual(result, "неуказанное будущее сокращение бюджета, особенно воображаемое сокращение.")

    def test_find_idiom_first_capital(self):
        result = self.engine.find_idiom("Magic asterisk")
        self.assertEqual(result, "неуказанное будущее сокращение бюджета, особенно воображаемое сокращение.")

    def test_find_idiom_uppercase(self):
        result = self.engine.find_idiom("Magic asterisk".upper())
        self.assertEqual(result, "неуказанное будущее сокращение бюджета, особенно воображаемое сокращение.")

    def test_find_idiom_mixed_up(self):
        result = self.engine.find_idiom("MaGIc AsTerIsk")
        self.assertEqual(result, "неуказанное будущее сокращение бюджета, особенно воображаемое сокращение.")

    def test_find_idiom_extra_spaces(self):
        result = self.engine.find_idiom(" MaGIc  AsTerIsk ")
        self.assertEqual(result, "Идиома не найдена")

    def test_find_idiom_with_none(self):
        with self.assertRaises(AttributeError):
            self.engine.find_idiom(None)

    def test_find_idiom_with_empty_string(self):
        result = self.engine.find_idiom("")
        self.assertEqual(result, "Идиома не найдена")

    def test_find_idiom_with_passing_digits(self):
        with self.assertRaises(AttributeError):
            self.engine.find_idiom(8888)


if __name__ == "__main__":
    main()
