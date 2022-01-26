import pyodbc
import pytest
import pandas as pd
import PythonTestAnswers as pta
import time

@pytest.mark.parametrize('file_location',[
        'https://github.com/mwez-priviahealth/data_engineering_assessment/raw/master/PythonTestQuestions/Privia%20Family%20Medicine%20113018.xlsx',
        r'C:\Users\vamsh\Downloads\Privia Family Medicine 113018.xlsx'])
class TestExcelFile:

    @pytest.mark.parametrize('sheet_name', ['Sheet1'])
    def test_import_excel(self, file_location, sheet_name):
        '''
        Checking to see if it handles both url and local file imports.
        Column comparision and row count
        '''
        expected_cols = ['ID', 'First Name', 'Middle Name', 'Last Name','DOB[1]', 'Sex', 'Favorite Color',
                         'Attributed Q1','Attributed Q2','Risk Q1','Risk Q2 ','Risk Increased Flag']
        temp_df = pta.import_excel(file_location, sheet_name)
        assert list(temp_df.columns) == expected_cols
        assert len(temp_df) == 100

    def test_extract_group_and_date(self, file_location):
        '''
        Testing both scenarios of url or local file path.
        '''
        expected_dict = {'provider_group_name' : 'Privia Family Medicine',
                         'file_date' : '11-30-2018'}
        file_info_dict = pta.extract_group_and_date(file_location)

        assert file_info_dict == expected_dict


@pytest.fixture
def query_sql_server():
    # Using factory design to allow parameters to be passed into fixture.
    def _query_sql_server(query):
        # Server and Database parameters will need to be updated based on individual environment
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                                    'SERVER=DESKTOP-QB0RL6F\SQLEXPRESS;'
                                    'DATABASE=Sandbox;'
                                    'Trusted_Connection=yes;')
        return pd.read_sql(query, connection)
    return _query_sql_server

@pytest.mark.parametrize('sample_df, table_name', [
    (
        pd.DataFrame({
            'Name':['Jane','Tom','Cecilia','Rodger'],
            'Age':[30,22,87,12]
        }), 'name_age'
    ),
    (
        pd.DataFrame({
            'Classes':['Science','Math','Trig','Chemistry'],
            'Student':['Jane','Tony','Sam','Chris']
        }), 'class_student'
    )
    ])
class TestDBConnection:
    def test_load_df_to_db(self, sample_df,table_name, query_sql_server):
        '''
        Testing column match
        '''
        query_cols = f'''
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA='dbo'
                '''
        pta.load_df_to_db(sample_df, 'DESKTOP-QB0RL6F\SQLEXPRESS', 'Sandbox', table_name,
                          'dbo')
        time.sleep(3) #Giving the database some time to update
        df = query_sql_server(query_cols)

        assert list(df['COLUMN_NAME']) == list(sample_df.columns)