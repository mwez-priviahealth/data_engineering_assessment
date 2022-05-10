#!/usr/bin/env python
# coding: utf-8

# # Instructions
# 	
#     NOTE: THIS SERVER CONNECTION IS DONE WITH MYSQL, NOT SQL SERVER
#     
#     In this directory you will find an Excel spreadsheet titled "Privia Family Medicine 113018.xlsx" containing demographics,
# 	quarter and risk data. We need this data to be manipulated and stored in our PersonDatabase for analysis.
# 	
# 
# 	Please include solutions to the questions below using Python 3.6 or higher.
# 	Please include any required modules in a "requirements.txt" file in this directory.
# 	Please provide adequate test coverage for you solutions.

#     1. Import the 'Demographics' data section to a table in the database. This ETL will need to process files of the same type delivered later on with different file dates and from different groups.
#     a. Include all fields under 'Demographics'
#     b. Define the sql schema as necessary. Fields should not include spaces or special characters.
#     c. Include fields in the data table that indicate the date of the file and the provider group located in the filename.
#         In this case "Privia Family Medicine" 11/30/2018. Assume the length of the group name will change and the date
#         will always be formatted at the end of the file as MMDDYY
#     d. Include only the first initial of the Middle Name when applicable.
#     e. Convert the Sex value to M or F: M for 0 and F for 1

# In[2]:


#imports
import pandas as pd
import pyodbc
import json
import os
import re


# # Question 1 - Upload and clean data

# In[3]:


#a. Include all fields under 'Demographics'
xl = 'Privia Family Medicine 113018.xlsx'
df = pd.read_excel(xl, header = 3, usecols =[1,2,3,4,5,6,7], skipfooter=3)

#b. Define the sql schema as necessary. Fields should not include spaces or special characters.
df = df.fillna(value=' ')
df.columns = df.columns.str.replace(' ','')
df = df.fillna(value='')
df['Favorite Color'] = ['' if x == 'Unknown' else x for x in df['Favorite Color']]

#c. Include fields in the data table that indicate the date of the file and the provider group located in the filename.
fileName = os.path.basename(xl)
fileName = str.replace(fileName,".xlsx","")
fileName = re.sub('[^a-zA-Z]+', ' ', fileName)



#d. Include only the first initial of the Middle Name when applicable.
df['MiddleName'] = df['MiddleName'].str[0]
df.columns = df.columns.str.replace('[^a-zA-Z^0-9]','')

#e. Convert the Sex value to M or F: M for 0 and F for 1
df['Sex'] = df.replace(0, 'M', inplace = True)
df['Sex'] = df.replace(1, 'F', inplace = True)

print(df)


# 
# 	2. Transform and import the 'Quarters' and 'Risk' data into a separate table.
# 	    a. Unpivot the data so that the data table includes
# 	        i. ID
# 	        ii. Quarter
# 	        iii. Attributed flag
# 	        iv. Risk Score
# 	        v. File date
# 	     b. Only include records in which the patients risk has increased.
# 	3. Include Unit Tests 
# 	4. Provide all necessary information for the team to get this up and running.

# # Question 2

# In[4]:



# Transform and import the 'Quarters' and 'Risk' data into a separate table.
quartersAndRisk = pd.read_excel(xl,header=3,usecols=[1,8,9,10,11,12],skipfooter=3)
quartersAndRisk.columns = quartersAndRisk.columns.str.replace(' ','')

#a. Unpivot the data so that the data table includes
quartersAndRisk = quartersAndRisk[ ['ID', 'AttributedQ1', 'AttributedQ2' , 'RiskQ1',  'RiskQ2']]
quartersAndRisk = pd.wide_to_long(quartersAndRisk, ["Attributed", "Risk"], i="ID", j="Quarter",suffix='\w+').reset_index()
print(quartersAndRisk)

# local server connection
pyodbcDrive = pyodbc.drivers()
print(pyodbcd)
driver = '{MySQL ODBC 3.51 Driver}'
server = 'input server here'
database = 'PersonDatabase'
connect = pyodbc.connect('DRIVER=' +driver+ ';SERVER='+server+';DATABASE='+database+';)
cursor = connect.cursor()

cursor.execute('''
		CREATE TABLE Demographics (ID int, FirstName nvarchar(255), MiddleName nvarchar(255), LastName nvarchar(255), DOB1 datetime,
			Sex varchar(1), FavoriteColor nvarchar(255), ProviderGroup nvarchar(1000), FileDate int
			)
               ''')
for row in df.itertuples():
  cursor.execute('''
                INSERT INTO Demographics (ID, FirstName, MiddleName ,LastName , DOB1 ,Sex , FavoriteColor ,ProviderGroup ,FileDate) VALUES (?,?,?,?,?,?,?,?,?)
                ''', row.ID, row.FirstName, row.MiddleName, row.LastName, row.DOB1, row.Sex, row.FavoriteColor, fname, filedate
                )
cursor.execute('''
		IF EXISTS (SELECT 1 FROM SYS.tables WHERE NAME = 'Quarters_Risk')
	DROP table Quarters_Risk
               ''')

cursor.execute('''
		CREATE TABLE Quarters_Risk (ID int, Quarter nvarchar(50), AttributedFlag nvarchar(50), Risk_Score float, FileDate int)
               ''')
for row in quartersAndRisk.itertuples():
  #print(row)
  cursor.execute('''
                INSERT INTO Quarters_Risk (ID, Quarter, AttributedFlag ,Risk_Score ,FileDate) VALUES (?,?,?,?,?)
                ''', row.ID, row.Quarter, row.Attributed, row.Risk, filedate
                )
connect.commit()


# In[ ]:


U

