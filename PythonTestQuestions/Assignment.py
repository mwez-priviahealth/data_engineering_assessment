import pandas as pd
import re
from sqlalchemy import create_engine
import unittest
import psycopg2
import openpyxl
engine = create_engine('postgresql://javierbenitez@localhost:5432/PERSONDATABASE')


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
    data['FILE_DATE'] = pd.to_datetime(data.FILE_DATE)
    data['FILE_DATE'] = data['FILE_DATE'].dt.date
    return data, file_name


# change the thing so it I used a pivot instead. make the dataframe its own function. Then pass it.
def upload_demographics():
    data, file_name = create_dataframe()
    data['SEX'] = data['SEX'].replace({0: 'M', 1: 'F'})
    data['MIDDLE_NAME'] = data['MIDDLE_NAME'].str[0]
    data['PROVIDER_GROUP'] = file_name[:-12]
    data = data.drop(['ATTRIBUTED_Q1', 'ATTRIBUTED_Q2', 'RISK_Q1', 'RISK_Q2', 'RISK_INCREASED_FLAG'], axis=1)
    data.to_sql('demographics', engine, if_exists='append')
    print(data)


def upload_quarterly_risk():
    data, file_name = create_dataframe()
    data.drop(data.columns[[1, 2, 3, 4, 5, 6, 7]], axis=1, inplace=True)
    indexes = data[data['RISK_INCREASED_FLAG'] == ' No'].index
    data.drop(indexes, inplace=True)
    data.drop(data.columns[3], axis=1, inplace=True)
    data.to_sql('quarterly_risk', engine, if_exists='append')
    print(data)

# Need to create test cases


def test_sum():
    assert sum([1, 2, 3]) == 6, "Should be 6"


def test_sum_tuple():
    assert sum((1, 2, 2)) == 5, "Should be 6"


def main():
    upload_demographics()
    upload_quarterly_risk()
    test_sum()
    test_sum_tuple()
    print("Everything passed")


main()
