import Python_Data_Assessment
import unittest

class test(unittest.TestCase):
    def testfilename(self):
        testing = Python_Data_Assessment.Assignment
        self.assertEqual(testing.getProviderGroup('asdfghjkl 123456.xlsx'), 'asdfghjkl')
        self.assertNotEqual(testing.getProviderGroup('asdfghjkl 123456.xlsx'), 'asdfg')
        self.assertEqual(testing.getProviderGroup('Privia Family Medicine 113018.xlsx'), 'Privia Family Medicine')

    def testdate(self):
        testing = Python_Data_Assessment.Assignment
        self.assertEqual(testing.getDate('asdfghjkl 123456.xlsx'), '123456')
        self.assertNotEqual(testing.getDate('asdfghjkl 123456.xlsx'), 'asdfg')
        self.assertEqual(testing.getDate('Privia Family Medicine 113018.xlsx'), '113018')