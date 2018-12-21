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
        self.assertEqual(self.lev.typeofdoc(), 'Двустороннее соглашение') 

    def test_area(self):
        self.assertEqual(self.lev.area(), 'Научно-техническое сотрудничество')

    def test_dates1(self):
        self.assertEqual(str(self.lev.get_dates()[0]), "1999-09-30")

    def test_dates2(self):
        self.assertEqual(str(self.lev.get_dates()[1]), "1997-11-21")

    def test_status(self):
        self.assertEqual(self.lev.status(), "Статус: Введен в действие")

    # test_keywords() & test_ngramms() return lists with different order because of using sets

if __name__ == '__main__':

    unittest.main()
