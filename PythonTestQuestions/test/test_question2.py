# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 00:01:10 2021

@author: Jacob Terrie
"""
import unittest
import pyodbc
import os
import argparse
import JacobTerriePythonQuestion2

#NOTE: To run scripts with SQL server, replace server name with appropriate value.
server = 'Server=FRASIER\SQLSERVERTEST;'

class QuestionIIUnitTest(unittest.TestCase):
     def setUp(self):
        self.testExcelFile = os.path.join(os.path.dirname(os.path.dirname(__file__)),"SampleDataFileQuestion2Privia Family Medicine 113018.xlsx")
    
     def test_extractdate01(self):
        file_name = "Privia Family Medicine.113018.xlsx"
        expected_output = ("113018")
        test_output = JacobTerriePythonQuestion2.extractProviderNameDate(file_name)
        self.assertEqual(expected_output,test_output)
        
     def test_extractdate02(self):
        file_name = "Privia Family Medicine.115518.xlsx"
        self.assertRaises(ValueError, JacobTerriePythonQuestion2.extractProviderNameDate, file_name)
        
     def test_SQLQueries1(self):
        parser = argparse.ArgumentParser(description = "Load data from Excel file into SQL Server.")
        parser.add_argument("--excelFile", 
                        type=str, #User types in the file name they want to add the SQL Server.
                        help="Inout Excel file that contains data to be loaded into SQL")
        parser.add_argument("--numRows",
                        type = int, #User types in the number of rows that are in the dataset.
                        required = True,
                        help = "Number of rows to add to database")
        numRows = 24
        args = parser.parse_args(["--excelFile",self.testExcelFile,"--numRows",str(numRows)])
        JacobTerriePythonQuestion2.main(args) #Should create Demographics table
        conn = pyodbc.connect('Driver={SQL Server};'
                      +server+
                      'Database=PersonDatabase;'
                      'Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT * FROM dbo.Patient_Risk_Assessment")
        distcount = 0
        queryrow = cursor.fetchall()
        for row in queryrow:
            distcount += 1
        self.assertEqual(distcount, 14)