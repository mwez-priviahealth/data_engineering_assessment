# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 23:05:40 2021

@author: Jacob Terrie
"""
import unittest
import pyodbc
import os
import argparse
import JacobTerriePythonQuestion1

#NOTE: To run scripts with SQL server, replace server name with appropriate value.
server = 'Server=FRASIER\SQLSERVERTEST;'

class QuestionIUnitTests(unittest.TestCase):
    
    def setUp(self):
        self.testExcelFile = os.path.join(os.path.dirname(os.path.dirname(__file__)),"SampleDataFileQuestion1Privia Family Medicine 113018.xlsx")
    
    def test_extractproviderdate01(self):
        file_name = "Privia Family Medicine.113018.xlsx"
        expected_output = ("Privia Family Medicine","113018")
        test_output = JacobTerriePythonQuestion1.extractProviderNameDate(file_name)
        self.assertEqual(expected_output,test_output)
        
    def test_extractproviderdate02(self):
        file_name = "Privia Family Medicine.122112.xlsx"
        expected_output = ("Privia Family Medicine","122112")
        test_output = JacobTerriePythonQuestion1.extractProviderNameDate(file_name)
        self.assertEqual(expected_output,test_output)
    
    def test_extractproviderdate03(self):
        file_name = "Privia Family Medicine.113218.xlsx"
        self.assertRaises(ValueError, JacobTerriePythonQuestion1.extractProviderNameDate, file_name)
     
    def test_SQLQueries1(self):
        parser = argparse.ArgumentParser(description = "Load data from Excel file into SQL Server.")
        parser.add_argument("--excelFile", 
                        type=str, #User types in the file name they want to add the SQL Server.
                        help="Inout Excel file that contains data to be loaded into SQL")
        parser.add_argument("--numRows",
                        type = int, #User types in the number of rows that are in the dataset.
                        required = True,
                        help = "Number of rows to add to database")
        numRows = 5
        args = parser.parse_args(["--excelFile",self.testExcelFile,"--numRows",str(numRows)])
        JacobTerriePythonQuestion1.main(args) #Should create Demographics table
        conn = pyodbc.connect('Driver={SQL Server};'
                      +server+
                      'Database=PersonDatabase;'
                      'Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT * FROM dbo.Demographics")
        distcount = 0
        queryrow = cursor.fetchall()
        for row in queryrow:
            distcount += 1
        self.assertEqual(distcount, numRows)