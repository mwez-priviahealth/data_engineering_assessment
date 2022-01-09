import pandas as pd
import numpy as np
import pandas.io.sql
import pyodbc

# create Connection and Cursor objects

DB = {'servername': 'DESKTOP-K3NHSRQ\SQLSERVER_2016',
      'database': 'PriviaHealth'}
# create the connection
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + DB['servername'] + ';DATABASE=' + DB['database'] + ';Trusted_Connection=yes')
cursor = conn.cursor()

# read data
file_path='C:\\Users\\DELL\\priviahealth\\'
file_name='Privia Family Medicine 113018.xlsx'
provider_group=file_name.split('.')[0][:-7]

file_date=file_name.split('.')[0][-6:]

file_location=file_path+file_name
data = pd.read_excel(file_location,skiprows=3,skipfooter=3).dropna(how='all', axis=1)

source_file_row_count=len(data.index)

demographics1=data[['ID', 'First Name', 'Middle Name', 'Last Name', 'DOB[1]', 'Sex','Favorite Color']]

demographics2=demographics1.assign( provider_group=provider_group )
demographics=demographics2.assign( file_date=file_date  )
demographics['Middle Name'] = demographics['Middle Name'].str[0]
demographics.rename(columns = {'Middle Name':'MI'}, inplace = True)

demographics = demographics.fillna(value=0)

quarters=data[['Attributed Q1', 'Attributed Q2']]
quarters=quarters.fillna(value=0)

risk=data[[ 'Risk Q1', 'Risk Q2 ', 'Risk Increased Flag']]
risk=risk.fillna(value=0)
#print(demographics.head(2))
# print(quarters.head(2))
# print(risk.head(2))

#create table if not exists

sql_createTable='''
IF NOT EXISTS (
SELECT * FROM information_schema.TABLES  
where TABLE_NAME='privia_demographics' and TABLE_SCHEMA='etl_stage'
)

CREATE TABLE [etl_stage].[privia_demographics] (
    ID varchar(20) not null,
    First_Name varchar(100),
    MI varchar(1),
    Last_Name varchar(100),
    DOB varchar(50),
    sex varchar(1),
    Favorite_Color varchar(50),
    provider_group varchar(50),
    file_date varchar(50),
    ETLInsertDT Datetime default getdate()
    )

IF NOT EXISTS (
SELECT * FROM information_schema.TABLES  
where TABLE_NAME='privia_quarters' and TABLE_SCHEMA='etl_stage'
)
CREATE TABLE [etl_stage].[privia_quarters] (
    Attributed_Q1 varchar(50),
    Attributed_Q2 varchar(50),
    ETLInsertDT datetime default getdate()
)


IF NOT EXISTS (
SELECT * FROM information_schema.TABLES  
where TABLE_NAME='privia_risk' and TABLE_SCHEMA='etl_stage'
)

CREATE TABLE [etl_stage].[privia_risk] (
    Risk_Q1 varchar(50),
    Risk_Q2 varchar(50),
    Risk_Increased_Flag varchar(50),
    ETLInsertDT datetime default getdate()
)'''

cursor.execute(sql_createTable)

# # Fetch all the records
# result = cursor.fetchall()
# for i in result:
#     print(i)
# cols = "','".join([str(i) for i in demographics.columns.tolist()])

for i,row in demographics.iterrows():
    sql = "INSERT INTO etl_stage.privia_demographics ( ID,First_Name,MI,Last_Name,DOB,sex, Favorite_Color,provider_group,file_date ) values(?,?,?,?,?,?,?,?,?)"
    cursor.execute(sql, row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
    conn.commit()
    
for i,row in quarters.iterrows():
    sql = "INSERT INTO etl_stage.privia_quarters ( Attributed_Q1,Attributed_Q2 ) values(?,?)"
    cursor.execute(sql, row[0],row[1])
    conn.commit()
   
for i,row in risk.iterrows():
    sql = "INSERT INTO etl_stage.privia_risk ( Risk_Q1,Risk_Q2,Risk_Increased_Flag ) values(?,?,?)"
    cursor.execute(sql, row[0],row[1],row[2])
    conn.commit()
   
conn.close()