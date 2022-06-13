from unittest import main
from unittest import TestCase

from backend.search_engine import SearchEngine


class LangDetectTest(TestCase):
    def test_lang_ru_upper(self):
        result = SearchEngine.lang_detect('ЧТОБЫ ПОВЕРИТЬ В ДОБРО, НАДО НАЧАТЬ ДЕЛАТЬ ЕГО.')
        self.assertEqual(result.value, 'ru')

    def test_lang_ru_lower(self):
        result = SearchEngine.lang_detect('Не откладывай до завтра, что можешь сделать сегодня.')
        self.assertEqual(result.value, 'ru')

    def test_lang_en_upper(self):
        result = SearchEngine.lang_detect('This allows you to use the shell filename to specify the module.'.upper())
        self.assertEqual(result.value, 'en')

    def test_lang_en_lower(self):
        result = SearchEngine.lang_detect('The unittest provides a set of tools for constructing and running tests.')
        self.assertEqual(result.value, 'en')

    def test_unsupported_lang(self):
        result = SearchEngine.lang_detect('La fête des Rois ou l’Épiphanie est célébrée dans toutes les églises chrétiennes.')
        self.assertEqual(result.value, 'fr')

    def test_passing_empty_string(self):
        with self.assertRaises(AttributeError):
            SearchEngine.lang_detect('')

    def test_passing_numbers(self):
        result = SearchEngine.lang_detect('8874887447521144')
        self.assertNotEqual(result.value, 'en')

    def test_passing_nothing(self):
        with self.assertRaises(TypeError):
            SearchEngine.lang_detect()

    def test_passing_invalid_string(self):
        result = SearchEngine.lang_detect("88558858551161")
        self.assertEqual(result.value, 'ja')

    def test_passing_two_values(self):
        with self.assertRaises(TypeError):
            SearchEngine.lang_detect('88941522228', 4848484)

    def test_passing_none(self):
        with self.assertRaises(AttributeError):
            SearchEngine.lang_detect(None)


if __name__ == '__main__':
    main()
