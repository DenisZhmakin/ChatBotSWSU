from unittest import main
from unittest import TestCase

from backend.search_engine import SearchEngine


class TestDictInfo(TestCase):
    def test_get_nouns(self):
        result = SearchEngine.get_word_info("Virus")
        self.assertEqual(result.speech_part, 'существительное')

    def test_get_verbs(self):
        result = SearchEngine.get_word_info("Make")
        self.assertEqual(result.speech_part, 'глагол')

    def test_adjective(self):
        result = SearchEngine.get_word_info("Colorful")
        self.assertEqual(result.speech_part, 'прилагательное')

    def test_non_speech_part(self):
        result = SearchEngine.get_word_info("aeveava")
        self.assertEqual(result.speech_part, '')

    def test_passing_digits(self):
        result = SearchEngine.get_word_info("88171")
        self.assertEqual(result.speech_part, '')

    def test_passing_two_values(self):
        with self.assertRaises(TypeError):
            SearchEngine.get_word_info("88171", 895)

    def test_empty_string(self):
        result = SearchEngine.get_word_info("")
        self.assertEqual(result, None)

    def test_passing_nothing(self):
        with self.assertRaises(TypeError):
            SearchEngine.get_word_info()

    def test_passing_numbers(self):
        res = SearchEngine.get_word_info(85558)
        self.assertNotEqual(res, "")

    def test_passing_sentence(self):
        res = SearchEngine.get_word_info("Is it a virus or not")
        self.assertNotEqual(res, "")

    def test_passing_none(self):
        res = SearchEngine.get_word_info(None)
        self.assertEqual(res, None)


if __name__ == '__main__':
    main()
