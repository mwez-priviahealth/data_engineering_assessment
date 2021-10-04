# -*- coding: utf-8 -*-

import pandas as pd
import pyodbc

#Connection details
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-KESK4OV;'
                      'Database=PersonDatabase;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

#RUN BELOW ONLY ONCE TO CREATE TABLE

##cursor.execute('''
##		CREATE TABLE Demographics (
##			ID int,
##			First_name nvarchar(50),
##           Middle_name nvarchar(1),
##            Last_name nvarchar(50),
##            DOB nvarchar(50),
##            Sex nvarchar(1),
##            Favorite_color nvarchar(50)
##			)
##               ''')
##conn.commit()

#Get data from excel
data = pd.read_excel (r'C:\Users\zts19\OneDrive\Desktop\Privia Family Medicine 113018.xlsx',
usecols="B:H",   #removing first column, selecting only Demographics
skiprows=(0,1,2) #Removing first 3 levels of headers
)
df = pd.DataFrame(data)

#Editing dataframe per conditions
df = df[0:100]#remove footer
df.columns = df.columns.str.replace(' ', '_')#remove spaces, insert underscores
df.columns = df.columns.str.replace('[', '')#removing [1] from DOB
df.columns = df.columns.str.replace('1]', '')#removing [1] from DOB
df = df.replace(',','', regex=True)#removing commas
df = df.replace(' ','', regex=True)#removing spaces
df = df.fillna('')#removing NaN 
df['Sex'] = df['Sex'].replace(0,'M', regex=True)#Replacing 0 with M in Sex field
df['Sex'] = df['Sex'].replace(1,'F', regex=True)#Replacing 1 with F in Sex field
df['Middle_Name']=df['Middle_Name'].str.slice(0,1)#Cutting Middle Names to one letter

#Inserting dataframe into table in db
for row in df.itertuples():
    cursor.execute('''
                INSERT INTO Demographics (ID, First_name, Middle_name, Last_name, DOB, Sex, Favorite_color)
                VALUES (?,?,?,?,?,?,?)
                ''',
                row.ID, 
                row.First_Name,
                row.Middle_Name,
                row.Last_Name,
                row.DOB,
                row.Sex,
                row.Favorite_Color
                )
conn.commit()
#Unfortunately I couldn't figure out how to parse the file name correctly to pull the date and 
#provider group, so I took it out in the interest of working code. Given more time I could get it.