import os
import re
import pandas as pd
import pyodbc
import json

# Question 1 - Upload and clean data

file = 'Privia Family Medicine 113018.xlsx'
df = pd.read_excel(file, header=3, usecols =[1,2,3,4,5,6,7], skipfooter=3)

df = df.fillna(value=' ')
df.columns = df.columns.str.replace(' ','')
df['Sex'] = ['M' if x == 0 else 'F' for x in df['Sex']]
df['MiddleName'] = df['MiddleName'].str[0]
df.columns = df.columns.str.replace('[^a-zA-Z^0-9]','')

df = df.fillna(value='')
df['FavoriteColor'] = ['' if x == 'Unknown' else x for x in df['FavoriteColor']]

print(df.head(10))

# Question 2- fname and file date
fname = os.path.basename(file)
fname = str.replace(fname,".xlsx","")
fname = re.sub('[^a-zA-Z]+', ' ', fname)
print(fname)

filedate = int("".join(filter(str.isdigit, file)))
print(filedate)

# Question 2-a
df_QR = pd.read_excel(file,header=3,usecols=[1,8,9,10,11,12],skipfooter=3)
df_QR.columns = df_QR.columns.str.replace(' ','')
pyodbcd = pyodbc.drivers()
print(pyodbcd)

df_QR=df_QR[ ['ID', 'AttributedQ1', 'AttributedQ2' , 'RiskQ1',  'RiskQ2']]
df_QR=pd.wide_to_long(df_QR, ["Attributed", "Risk"], i="ID", j="Quarter",suffix='\w+').reset_index()
print(df_QR)

# connecting to local server
server = 'Server=DESKTOP-Q05NEKA\kreem;'
connection = pyodbc.connect('Driver={SQL Server};' 'Server=DESKTOP-Q05NEKA\kreem;' 
                    'Database=PersonDatabase;'
                    'Trusted_Connection=yes;')
cursor = connection.cursor()

# Create Demographics Table
cursor.execute('''
		CREATE TABLE Demographics (ID int, FirstName nvarchar(255), MiddleName nvarchar(255), LastName nvarchar(255), DOB1 datetime,
			Sex varchar(1), FavoriteColor nvarchar(255), ProviderGroup nvarchar(1000), FileDate int
			)
               ''')
print('Demographics Table Exists')

# insert into python syntax
for row in df.itertuples():
      #print(row)
  cursor.execute('''
                INSERT INTO Demographics (ID, FirstName, MiddleName ,LastName , DOB1 ,Sex , FavoriteColor ,ProviderGroup ,FileDate) VALUES (?,?,?,?,?,?,?,?,?)
                ''', row.ID, row.FirstName, row.MiddleName, row.LastName, row.DOB1, row.Sex, row.FavoriteColor, fname, filedate
                )
print('Demographics Table Filled')

# drop table python syntax -- for later files
cursor.execute('''
		IF EXISTS (SELECT 1 FROM SYS.tables WHERE NAME = 'Quarters_Risk')
	DROP table Quarters_Risk
               ''')
print('Quarters_Risk Table Dropped')


# create table python syntax
cursor.execute('''
		CREATE TABLE Quarters_Risk (
			ID int,
			Quarter nvarchar(50),
			AttributedFlag nvarchar(50),
			Risk_Score float,
			FileDate int
			)
               ''')
print('Quarters_Risk Table Created')


# Insert into syntax python
for row in df_QR.itertuples():
  #print(row)
  cursor.execute('''
                INSERT INTO Quarters_Risk (ID, Quarter, AttributedFlag ,Risk_Score ,FileDate) VALUES (?,?,?,?,?)
                ''', row.ID, row.Quarter, row.Attributed, row.Risk, filedate
                )
print('Quarters_Risk Table is Populated')

connection.commit()