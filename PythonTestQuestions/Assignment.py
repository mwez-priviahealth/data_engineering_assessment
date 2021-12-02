import pandas as pd
import re
import psycopg2
import openpyxl

def create_dataframe():
    file_name = 'Privia Family Medicine 113018.xlsx'
    data = pd.read_excel(file_name, header=3, usecols='B:M', index_col='ID')
    data = data.dropna(subset=['First Name', 'Sex'])
    new_headers = []
    header = data.columns
    for name in header:
        name = re.sub('[^A-Za-z0-9]+', ' ', name)
        new_name = name.upper()
        new_name = new_name.replace(' ', '_')
        new_name = new_name.rstrip('_')
        new_headers.append(new_name)
    print(new_headers)
    data.columns = new_headers
    data['FILE_DATE'] = (file_name[-12:-5])
    return data, file_name


#change the thing so it I used a pivot instead. make the dataframe its own function. Then pass it.
def upload_demographics():
    data, file_name = create_dataframe()
    data['SEX'] = data['SEX'].replace({0: 'M', 1: 'F'})
    data['MIDDLE_NAME'] = data['MIDDLE_NAME'].str[0]
    data['PROVIDER_GROUP'] = file_name[:-12]
    data = data.drop(['ATTRIBUTED_Q1', 'ATTRIBUTED_Q2', 'RISK_Q1', 'RISK_Q2', 'RISK_INCREASED_FLAG'], axis=1)
    data.to_sql()
    print(data)

def upload_quarterly_risk():
    data, file_name = create_dataframe()
    data.drop(data.columns[[1,2,3,4,5,6,7]], axis=1, inplace=True)
    indexes = data[data['RISK_INCREASED_FLAG'] == ' No'].index
    data.drop(indexes, inplace=True)
    data.drop(data.columns[3], axis=1, inplace=True)
    print(data)

def main():
    upload_demographics()
    upload_quarterly_risk()
main()