import pandas as pd
import pyodbc as odbc
import os
from datetime import datetime

#====================
#Extract file
#====================

#Specify file path and server name below.  Looks for any .xlsx file.  Saves file name to var.
dir = 'C:/Users/Administrator/Desktop/Privia/Inbound/'
server_name = 'EC2AMAZ-63084T8'

try:
    #Look for any XLSX in specified directory
    for source_file in os.listdir (dir):
        if source_file.endswith ('.xlsx'):
            df_demo = pd.read_excel(dir+source_file,header=3,usecols=[1,2,3,4,5,6,7],skipfooter=3)
            df_quar = pd.read_excel(dir+source_file,header=3,usecols=[1,8,9,10,11,12],skipfooter=3)
            file_name = str.replace(source_file,".xlsx","")
    if 'file_name' not in locals():
        raise Exception("No XLSX in dir")
    #Get ProviderGroup
    ProviderGroup = file_name[:-7]
    #Get FileDate
    FileDate = file_name[-6:]
    FileDate = datetime.strptime(FileDate, '%m%d%y').strftime('%m/%d/%Y')
    print("File extracted")
except:
    print('Could not extract file')
    exit()

#====================
# Transform Data
#====================

try:
    #====================
    # Transform Data Demographics
    #====================
    #Fix column names to remove spaces, special chars, nums.
    df_demo.rename(columns={"First Name": "FirstName", "Middle Name": "MiddleName", "Last Name": "LastName", "DOB[1]": "DOB", "Favorite Color": "FavoriteColor"}, inplace = True)

    #remove nan, format middle name, format sex
    df_demo.fillna('', inplace = True)
    df_demo['MiddleName'] = df_demo['MiddleName'].str[0]
    df_demo['Sex'] = ['M' if x == 0 else 'F' for x in df_demo['Sex']]

    #====================
    # Transform Quarter Risk
    #====================

    #Fix column names to remove spaces, special chars, nums.
    df_quar.rename(columns={"Attributed Q1": "AttributedQ1", "Attributed Q2": "AttributedQ2", "Risk Q1": "RiskQ1", "Risk Q2 ": "RiskQ2", "Risk Increased Flag": "RiskIncreasedFlag"}, inplace = True)

    # Filter Data for Only records_demo in which the patients risk has increased.
    df_quar=df_quar[df_quar['RiskIncreasedFlag']=='Yes']
    #drop risk increasing column
    df_quar=df_quar[ ['ID', 'AttributedQ1', 'AttributedQ2' , 'RiskQ1',  'RiskQ2']] 

    #Unpivot
    df_quar=pd.wide_to_long(df_quar, ["Attributed", "Risk"], i="ID", j="Quarter",suffix='\w+').reset_index()
    
    #====================
    #DF to lists for Insert
    #====================

    #Append Provider and Date to DFs
    df_demo["ProviderGroup"] = ProviderGroup
    df_demo["FileDate"] = FileDate
    df_quar["FileDate"] = FileDate

    df_demo.fillna('',inplace=True)
    records_demo = df_demo.values.tolist()
    records_quar = df_quar.values.tolist()

    print('Data Transformed')

except:
    print('Could not transform data')
    exit()

#====================
#Create SQL Server Connection
#====================

#Update server info below:
conn_string =   'DRIVER={SQL Server};SERVER='+server_name+';DATABASE=PersonDatabase;Trust_Connection=yes;'

try:
    conn = odbc.connect(conn_string)
except:
    print('SQL Connection Error')
    exit()

#====================
#Define SQL
#====================

#Drop and recreate_demo Table
recreate_demo = ''' 
            IF EXISTS (SELECT * FROM SYSOBJECTS WHERE NAME = 'Demographics')
                DROP TABLE Demographics 
                                 
            CREATE TABLE [dbo].Demographics
            (
                ID					int
                ,FirstName			varchar(100)	
                ,MiddleName			varchar(100)
                ,LastName			varchar(100)
                ,DOB				datetime 
                ,Sex				varchar(100)
                ,FavoriteColor		varchar(100)
                ,ProviderGroup		varchar(100)
                ,FileDate			date 
            )  
           '''

#Insert
sql_insert_demo =    '''
                INSERT INTO Demographics (ID, FirstName, MiddleName ,LastName , DOB, Sex, FavoriteColor ,ProviderGroup ,FileDate)
                VALUES (?,?,?,?,?,?,?,?,?)
                '''

recreate_quar = '''
            IF EXISTS (SELECT * FROM SYSOBJECTS WHERE NAME = 'Quarter_Risk')
                DROP TABLE Quarter_Risk 

           CREATE TABLE [dbo].[Quarter_Risk]
           (
                [ID]			int 
                ,[Quarter]		[varchar](100) 
                ,[Attributed]	[varchar](100) 
                ,[Risk]			float 
                ,[FileDate]     date 
            )
            '''

sql_insert_quar = '''
            INSERT INTO [Quarter_Risk] (ID, [Quarter], Attributed ,Risk , FileDate)
                VALUES (?,?,?,?,?)
            '''

#====================
#Create a cursor connection and insert records
#====================

try:
    cursor = conn.cursor()
    cursor.execute(recreate_demo)
    cursor.executemany(sql_insert_demo,records_demo)
    cursor.execute(recreate_quar)
    cursor.executemany(sql_insert_quar,records_quar)
    cursor.commit();  
    print('Records have been loaded')  
except:
    cursor.rollback()
    print('Could not insert records')
finally:
    cursor.close()
    conn.close()  
