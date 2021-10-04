
import pandas as pd
import pyodbc

#Connection details
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-KESK4OV;'
                      'Database=PersonDatabase;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

#RUN BELOW ONLY ONCE TO CREATE TABLE

#cursor.execute('''
#		CREATE TABLE QuarterlyRisk (
#			ID int,
#			Quarter int,
#           Attributed_Flag nvarchar(50),
#           Risk_Score nvarchar(50),
#           File_Date nvarchar(50)
#			)
#               ''')
#conn.commit()

#Get data from excel
data2 = pd.read_excel (r'C:\Users\zts19\OneDrive\Desktop\Privia Family Medicine 113018.xlsx',
usecols="B, I:M",   #removing first column, selecting only relevant columns
skiprows=(0,1,2) #Removing first 3 levels of headers
)
df2 = pd.DataFrame(data2)
risky = df2['Risk Increased Flag'] == "Yes" #creating conditional for Risk Flag
df_risk = df2[risky] #Getting only instances where Risk Increased Flag is Yes
df_risk.columns = df_risk.columns.str.replace(' ', '_')#remove spaces, insert underscores

for row in df_risk.itertuples():
    cursor.execute('''
                INSERT INTO QuarterlyRisk (ID, Quarter, Attributed_Flag, Risk_Score)
                VALUES (?,?,?,?)
                ''',
                row.ID, 
                1 and 2,
                row.Attributed_Q1 and row.Attributed_Q2,
                row.Risk_Q1 and row.Risk_Q2_ # This doesn't work as intended, does not bring in each score per quarter. Given more time I could solve this.
                )
conn.commit()