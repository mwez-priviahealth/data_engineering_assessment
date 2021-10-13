# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 19:37:49 2021

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
    provider = providername[:-7] #Extracts the name
    return (provider, date)

def main(args):
    #Extract provider and date from excel file
    provider, date = extractProviderNameDate(args.excelFile)
    date = date[0:2] + "/" + date[2:4] + "/" + date[4:]
    print(f"Provider Name extracted {provider}....")
    print(f"Date extracted {date}....")
    numRows = int(args.numRows)
    
    #This connects to the SQL server
    conn = pyodbc.connect('Driver={SQL Server};'
                      +server+
                      'Database=PersonDatabase;'
                      'Trusted_Connection=yes;')
    cursor = conn.cursor()

    #Create database with certain columns as defined by excel sheet. 
    #You only need to use once when adding to the SQL server
    cursor.execute(''' if not exists (SELECT * FROM sysobjects where name = 'Demographics' and xtype = 'U')
    		CREATE TABLE Demographics (
     			ID int,
     			First_name nvarchar(50),
                Middle_name nvarchar(1),
                Last_name nvarchar(50),
                DOB nvarchar(50),
                Sex nvarchar(1),
                Favorite_color nvarchar(50),
                Provider nvarchar(50),
                DateTime nvarchar(50)
     			)
                    ''')
    conn.commit()
    Data = pd.read_excel (args.excelFile, usecols="B:H",
                          skiprows=(0,1,2), #Removing first 3 levels of headers
                          nrows = numRows
                          ) #This will only include the demographics columns.
    rows = Data.to_csv(index = 0, header = False).split("\r\n")[:-1]
    for idx in range(len(rows)):
        row = rows[idx].split(",")
        row[5] = "F" if int(row[5]) == 1 else 'M' #Convnerts numerical values in the sex column to string values. 1 for Female, 0 for Male
        
        if row[2] != '':
            row[2] = row[2][0]
        cursor.execute("""INSERT INTO dbo.Demographics(ID, First_name, Middle_name, Last_name, DOB, Sex, Favorite_color, Provider, DateTime)
                       VALUES(?,?,?,?,?,?,?,?,?)""",row[0],row[1],row[2],row[3],row[4],row[5],row[6],provider,date)
    conn.commit()
    cursor.close()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Load data from Excel file into SQL Server.")
    parser.add_argument("--excelFile", 
                        type=str, #User types in the file name they want to add the SQL Server.
                        help="Inout Excel file that contains data to be loaded into SQL")
    parser.add_argument("--numRows",
                        type = int, #User types in the number of rows that are in the dataset.
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