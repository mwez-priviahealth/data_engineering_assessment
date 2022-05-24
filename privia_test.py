import pandas as pd
import numpy as npy
import pyodbc 
import sys
print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))
if len(sys.argv)<=1 and len(sys.argv)>=3 :
    print("Invalid number of Arguments")
    exit()


def first1(s):
    return s[:1]


def sex(s):
    ret1 = str(s).replace('0', 'M')
    ret2 = ret1.replace('1', 'F')
    return ret2

folder_path=sys.argv[1]
file_name=sys.argv[2]
demographic_data=pd.read_excel(folder_path+file_name,header=3,na_values=['NA'], usecols="B,C:H" ,skipfooter=3);
demographic_data1=demographic_data.replace(npy.nan,'',regex=True)
msconn = pyodbc.connect('Driver={SQL Server};'                      'Server=DESKTOP-VJI8J3Q;'                      'Database=persondatabase;'                      'Trusted_Connection=yes;')
cursor = msconn.cursor()

df = pd.read_excel(folder_path+file_name,header=3,na_values=['NA'], usecols="B,I:M" ,skipfooter=3);
df_risk_q = df.melt(id_vars = 'ID', value_vars = ['Attributed Q1', 'Attributed Q2'], var_name = 'Quarters', value_name = 'Attributed_flag')
df_risk_r = df[df['Risk Increased Flag'] == 'Yes']
df_risk_r = df_risk_r.melt(id_vars = 'ID', value_vars = ['Risk Q1', 'Risk Q2 '], var_name = 'Risk Data', value_name = 'Risk_score')
df_risk = pd.merge(df_risk_q, df_risk_r, how="inner",  on='ID')


print(df_risk)

for index, row in df_risk.iterrows():
    cursor.execute("INSERT INTO dbo.Risk_PY (PersonID,Quarter,Attributed_flag,RiskScore,FileDate) values(?,?,?,?,?)",row['ID'],row['Quarters'],row['Attributed_flag'],row['Risk_score'],file_name[-11:-5])
    msconn.commit()

for index, row in demographic_data1.iterrows():

    cursor.execute("INSERT INTO dbo.demographics (ID , First_Name , Middle_Name , Last_Name	    , DOB             , Sex             , Favorite_Color  , provider_group  , group_file_date ) values(?,?,?,?,?,?,?,?,?)",row['ID'],row['First Name'],first1(row['Middle Name']),row['Last Name'],row['DOB[1]'],sex(row['Sex']),row['Favorite Color'], file_name[0:-11],file_name[-11:-5])

    msconn.commit()
cursor.close()