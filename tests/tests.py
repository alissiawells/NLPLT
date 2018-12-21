import unittest
import leviafunc as lf
import os

class TestLeviafunc(unittest.TestCase):

    def setUp(self): 
        self.lev = lf.Leviafunc('testdoc.txt') 

    def test_title(self):
        self.assertEqual(self.lev.title(), 'СОГЛАШЕНИЕ между Правительством Российской Федерации и Правительством Федеративной Республики Бразилии о научно-техническом сотрудничестве \n')

    def test_countries(self):
       self.assertEqual(self.lev.countries_print()[0], 'Бразилия')

    def test_typeofdoc(self):
        self.assertEqual(self.lev.typeofdoc(), 'Двустороннее соглашение \n') 

    def test_area(self):
        self.assertEqual(self.lev.area(), 'Научно-техническое сотрудничество')

    def test_dates1(self):
        self.assertEqual(str(self.lev.get_dates()[0]), "1999-09-30")

    def test_dates2(self):
        self.assertEqual(str(self.lev.get_dates()[1]), "1997-11-21")

    def test_keywords(self):
        keywords = ['область_наука_', 'вступать_сила_', 'оба_страна_', 'настоящее_соглашение_', 'сотрудничество_область_', 'интеллектуальный_собственность_', 'сотрудничество_рамка_', 'российский_федерация_', 'федерация_правительство_', 'правительство_российский_', '_год_', 'прекращение_действие_', 'научнотехнический_сотрудничество_', 'распределение_право_', 'договариваться_сторона_', 'соглашение_научнотехнический_', 'научнотехнический_информация_', 'настоящий_соглашение_', 'наука_техника_', 'рамка_настоящий_', 'бразилия_апрель_', '_год_', 'декабрь__', 'научнотехнический_сотрудничество_', 'бразилиа_ноябрь_', 'результат_сотрудничество_']
        self.assertEqual(self.lev.keywords(), keywords)

    def test_ngramms(self):
        ngramms = ['информация', 'страна', 'координация', 'бразилия', 'сторона', 'каждый', 'ассоциация', 'свой', 'сотрудничество', 'правительство', 'действие', 'проект', 'бразилиа', 'комиссия', 'отношение', 'рекомендация', 'организация', 'соглашение', 'реализация', 'федеративный', 'сила', 'федерация', 'настоящий', 'научнотехнический', 'настоящее', 'республика']
        self.assertEqual(self.lev.keyphrases(), ngramms)

    def test_status(self):
        self.assertEqual(self.lev.status(), "Статус: Введен в действие")

if __name__ == '__main__':

    unittest.main()
