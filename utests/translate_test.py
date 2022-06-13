from unittest import TestCase, main

from backend.search_engine import SearchEngine


class TranslateTest(TestCase):
    def setUp(self):
        self.engine = SearchEngine()

    def test_from_ru_to_en(self):
        result = self.engine.get_translate("Человек ощущает себя частью природы, частью всего, что живет на Земле.")
        self.assertEqual(result, "A person feels himself a part of nature, a part of everything that lives on Earth.")

    def test_from_en_to_ru(self):
        text = "If advertisements are to he learned, there is a need for lots of repetition."
        result = self.engine.get_translate(text)
        self.assertEqual(result, "Если реклама должна быть изучена, необходимо много повторений.")

    def test_unsupported_language(self):
        text = "La fête des Rois ou l’Épiphanie est célébrée dans toutes les églises chrétiennes."
        result = self.engine.get_translate(text)
        self.assertEqual(result, "Поддержка данного языка (fr) не реализована")

    def test_passing_empty_string(self):
        with self.assertRaises(AttributeError):
            self.engine.get_translate("")

    def test_passing_digits(self):
        with self.assertRaises(TypeError):
            self.engine.get_translate(985741)

    def test_passing_nothing(self):
        with self.assertRaises(TypeError):
            self.engine.get_translate()

    def test_passing_invalid_string(self):
        result = self.engine.get_translate('88941522228')
        self.assertEqual(result, "Поддержка данного языка (ja) не реализована")

    def test_passing_two_values(self):
        with self.assertRaises(TypeError):
            self.engine.get_translate('88941522228', 4848484)

    def test_passing_none(self):
        with self.assertRaises(AttributeError):
            self.engine.get_translate(None)


if __name__ == '__main__':
    main()
