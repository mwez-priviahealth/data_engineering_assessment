# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 21:25:35 2021

@author: Jacob Terrie
"""
#NOTE: To run scripts with SQL server, replace server name with appropriate value.
server = 'Server=FRASIER\SQLSERVERTEST;'

import pandas as pd
import pyodbc
import os
import argparse
import sys

def extractProviderNameDate(file):
    base_name = os.path.basename(file)
    providername, ext = os.path.splitext(base_name);
    date = providername[-6:] #Extracts the date
    if not(int(date[0:2]) > 0) or not (int(date[2:4]) <= 30): #checks for valid month in date string
        print("Invalid Date.")
        raise ValueError
    return date

def main(args):
    #Extract provider and date from excel file
    date = extractProviderNameDate(args.excelFile)
    date = date[0:2] + "/" + date[2:4] + "/" + date[4:]
    print(f"Date extracted {date}....")
    numRows = int(args.numRows)
    
    #Create database with certain columns as defined by excel sheet.
    #This connects to the SQL server
    conn = pyodbc.connect('Driver={SQL Server};'
                      +server+
                      'Database=PersonDatabase;'
                      'Trusted_Connection=yes;')
    cursor = conn.cursor()

    #RUN BELOW ONLY ONCE TO CREATE TABLE

    cursor.execute(''' if not exists (SELECT * FROM sysobjects where name = 'Patient_Risk_Assessment' and xtype = 'U')
    		CREATE TABLE Patient_Risk_Assessment (
     			ID int,
              Attributed_Q1 nvarchar(10),
              Attributed_Q2 nvarchar(10),
              Risk_Score_Q1 float(10),
              Risk_Score_Q2 float(10),
              Increased_Risk_Flag nvarchar(10),
              DateTime nvarchar(50)
     			)
                    ''')
    conn.commit()
    PatientIDDataFrame = pd.read_excel (args.excelFile, usecols="B",
                          skiprows=(0,1,2), #Removing first 3 levels of headers
                          nrows = numRows
                          ) #This will only include the patient ID columns.
    rows = PatientIDDataFrame.to_csv(index = False, header = False).split("\r\n")[:-1]
    patientID = []
    
    for idx in range(len(rows)):
        row = rows[idx].split(",")
        patientID.append(int(row[0]))
      
    QuartRisk = pd.read_excel (args.excelFile, usecols="I:M",
                          skiprows=(0,1,2), #Removing first 3 levels of headers
                          nrows = numRows
                          ) #This will only include the quarter and risk data columns.
    QD = QuartRisk.to_csv(index = False, header = False).split("\r\n")[:-1]
    
    for idx in range(len(QD)):
        QDX = QD[idx].split(",")
        if QDX[4].strip() == "No":
            continue
        cursor.execute("""INSERT INTO dbo.Patient_Risk_Assessment(ID, Attributed_Q1, Attributed_Q2, Risk_Score_Q1, Risk_Score_Q2, Increased_Risk_Flag, DateTime)
                       VALUES(?,?,?,?,?,?,?)""",patientID[idx],QDX[0],QDX[1],QDX[2],QDX[3],QDX[4],date)
    conn.commit()
    cursor.close()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Load data from Excel file into SQL Server.")
    parser.add_argument("--excelFile", 
                        type=str, #User types in the file name they want to add the SQL Server.
                        help="Inout Excel file that contains data to be loaded into SQL")
    parser.add_argument("--numRows",
                        type = int,
                        required = True,
                        help = "Number of rows to add to database")
    args = parser.parse_args()
    
    if args.excelFile is None:
        parser.print_help()
        sys.exit(0)
        
    if not os.path.exists(args.excelFile):
        parser.print_help()
        sys.exit(0)
        
    main(args)