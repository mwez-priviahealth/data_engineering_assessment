import unittest
from Assignment import upload_quarterly_risk

class MyTestCase(unittest.TestCase):

    def test_something(self):
        data = upload_quarterly_risk()
        self.assertEqual(len(data['FILE_DATE']), 53), 'Tests the length of the Dataframe'


if __name__ == '__main__':
    unittest.main()
