import pyodbc
import pandas as pd
from datetime import datetime


class Assignment:
    try:
        sql_conn = pyodbc.connect('Driver={SQL Server};'
                                  'Server=localhost;'
                                  'Database=PersonDatabase;'
                                  'Trusted_Connection=yes;')

        cursor = sql_conn.cursor()


        cursor.execute('''
                        IF NOT EXISTS(SELECT 1 FROM sys.Tables
                        WHERE Name = N'Demographics')
                        BEGIN
                            CREATE TABLE dbo.Demographics (
                              ID VARCHAR(255) PRIMARY KEY,
                              FirstName VARCHAR(255),
                              MiddleName CHAR,
                              LastName VARCHAR(255),
                              DateOfBirth DATE,
                              Sex CHAR,
                              FavoriteColor VARCHAR(255),
                              ProviderGroup VARCHAR(255),
                              FileCreatedDate DATE)
                              END''')


        cursor.execute('''
                        IF NOT EXISTS(SELECT 1 FROM sys.Tables
                        WHERE Name = N'Quarters')
                        BEGIN
                            CREATE TABLE dbo.Quarters (
                                ID VARCHAR(255), 
                                Quarter VARCHAR(10), 
                                Attributed VARCHAR(10), 
                                Risk FLOAT(15), 
                                FileCreatedDate DATE)
                                END''')

        sql_conn.commit()

    except:
        "Failed to connect to server."
        exit()


    # Start Demographic data transformation
    Demographics = pd.read_excel('Privia Family Medicine 113018.xlsx', skiprows=3, usecols=range(1,8))

    # Drop the last three rows
    Demographics.drop(Demographics.tail(3).index,
            inplace = True)

    # Change full middle name to middle initial where applicable
    Demographics['Middle Name'] = Demographics['Middle Name'].str[0]

    # Transform date of birth to target format
    Demographics['DOB[1]'] = Demographics['DOB[1]'].dt.strftime('%Y-%m-%d')

    # Transform gender
    Demographics['Sex'].replace(0, 'M',inplace=True)
    Demographics['Sex'].replace(1, 'F',inplace=True)


    # Including fields in table that indicate the date of the file and the provider group
    # Creating functions for unit tests
    filename = 'Privia Family Medicine 113018.xlsx'
    def getProviderGroup(filename):
        return filename[:-12]

    ProviderGroup = getProviderGroup(filename)
    Demographics['ProviderGroup'] = ProviderGroup

    def getDate(filename):
        return filename[-11:][:6]


    Date = datetime.strptime(getDate(filename), '%m%d%y').strftime('%Y-%m-%d')

    Demographics['FileCreatedDate'] = Date
    Demographics['FileCreatedDate'] = pd.to_datetime(Demographics['FileCreatedDate'])

    # Replace nan to None
    Demographics = Demographics.where(pd.notnull(Demographics), None)

    # Start Quarters data transformation
    Quarters = pd.read_excel('Privia Family Medicine 113018.xlsx', skiprows=3, usecols=range(1,13))

    # Specify the necessary columns
    cols = [0,7,8,9,10,11]
    Quarters = Quarters[Quarters.columns[cols]]

    # Drop last three rows
    Quarters.drop(Quarters.tail(3).index,
            inplace = True)

    # Drop records where the patients risk did not increase
    Quarters = Quarters[Quarters['Risk Increased Flag'] == 'Yes']

    # Add date to table
    Quarters['FileCreatedDate'] = Demographics['FileCreatedDate']

    # Import Demographics data to Demographics table
    for index, row in Demographics.iterrows():
        cursor.execute("INSERT INTO dbo.Demographics (ID,FirstName,MiddleName,LastName,DateOfBirth,Sex,FavoriteColor,ProviderGroup,FileCreatedDate) values(?,?,?,?,?,?,?,?,?)",
                       row['ID'],
                       row['First Name'],
                       row['Middle Name'],
                       row['Last Name'],
                       row['DOB[1]'],
                       row['Sex'],
                       row['Favorite Color'],
                       row['ProviderGroup'],
                       row['FileCreatedDate'])

    # Import Quarter 1 and Risk Q1 data to Quarters table
    for index, row in Quarters.iterrows():
        cursor.execute("INSERT INTO dbo.Quarters (ID,Quarter,Attributed,Risk,FileCreatedDate) values(?,?,?,?,?)",
                       row['ID'],
                       'Q1',
                       row['Attributed Q1'],
                       row['Risk Q1'],
                       row['FileCreatedDate'])


    # Import Quarter 2 and Risk Q2 data to Quarters table
    for index, row in Quarters.iterrows():
        cursor.execute("INSERT INTO dbo.Quarters (ID,Quarter,Attributed,Risk,FileCreatedDate) values(?,?,?,?,?)",
                       row['ID'],
                       'Q2',
                       row['Attributed Q2'],
                       row['Risk Q2 '],
                       row['FileCreatedDate'])
    sql_conn.commit()
    cursor.close()