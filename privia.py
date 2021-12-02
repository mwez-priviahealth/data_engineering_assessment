import os
import pandas as pd



## GET FILENAME AND DATE ##

fullpath = '/Users/melissa/Desktop/data_engineering_assessment-master/PythonTestQuestions/Privia Family Medicine 113018.xlsx' #insert correct filepath

path, filename = os.path.split(fullpath)
root, ext = os.path.splitext(filename)
group = ' '.join(filename.split(' ')[:-1])
filedate = root.rsplit(' ')[3]

#print(group)
#print(filedate)



## LOAD DATA FILE ##


df = pd.read_excel(fullpath, usecols="B:M", skiprows=3) #insert correct filepath


## TRANSFORM DATA ##

df.columns = df.columns.str.replace(' ', '')

df.rename(columns={'DOB[1]': 'DOB'}, inplace=True)
df['DOB'] = pd.to_datetime(df.DOB)

df['MiddleName'] = df['MiddleName'].str[:1]

df.insert(7, "ProviderGroup", group)
df.insert(8, "FileDate", filedate)

df['FileDate'] = pd.to_datetime(df.FileDate)
df['FileDate'] = df['FileDate'].dt.strftime('%m/%d/%Y')
df['Sex'] = df['Sex'].astype(str)
df['Sex'] = df['Sex'].str.replace("0","M")
df['Sex'] = df['Sex'].str.replace("1","F")
df['Sex'] = df['Sex'].str[:1]

print("\n")
print('Transformed Data: ')

print(df.head())



## CREATE DEMOGRAPHICS TABLE ##


dcols = df[['ID', 'FirstName', 'MiddleName', 'LastName', 'DOB', 'Sex', 'FavoriteColor', 'ProviderGroup', 'FileDate']]

demographics = dcols.copy()

print("\n")
print('Demographics Table: ')
print(demographics.head())


## CREATE QUARTER AND RISK TABLE ##


qcols = df[['ID','AttributedQ1','AttributedQ2', 'RiskQ1', 'RiskQ2', 'RiskIncreasedFlag','FileDate']]
quartersrisks =  qcols.copy()
quartersrisks = quartersrisks.loc[quartersrisks['RiskIncreasedFlag'] == 'Yes']

print("\n")
print('Quarter and Risk Table: ')
print(quartersrisks.head())
