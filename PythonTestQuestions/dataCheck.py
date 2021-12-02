import unittest
import math
from Assignment import upload_demographics


class test_length(unittest.TestCase):
    def test_demographics(self):
        data = upload_demographics()
        self.assertEqual((math.isnan(data['MIDDLE_NAME'][0])), True), "Blanks are NaNs"
        self.assertEqual(len(data['MIDDLE_NAME'][3]), 1), "Length is 1"
        self.assertEqual((data['SEX'][0]), 'M'), "Men are M"
        self.assertEqual((data['SEX'][2]), 'F'), "Women are F"
        self.assertEqual(str(data['FILE_DATE'][0]), '2018-11-30'), "Transformed Date"
        self.assertEqual(str(data['PROVIDER_GROUP'][0]), 'Privia Family Medicine'), "Provider Name"


# class test_upload_quarterly_risk(unittest.TestCase):
#     def test_middle_name_length(self):
#         self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
