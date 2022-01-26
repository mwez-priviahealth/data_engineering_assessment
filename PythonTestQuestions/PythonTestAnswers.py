import pandas as pd
import sqlalchemy
import os
import datetime
import pyodbc


def import_excel(file_path: str, sheet_name: str) -> pd.DataFrame:
    """
    Reads through an excel file and returns a dataframe.

    :param file_path: Location of the excel file; it can be a file path on local machine, or url direclty to the file.
    :param sheet_name: Name of the sheet where the data is stored
    :return: Returns a formatted dataframe of the excel input. Unnecessary header/footer rows are removed.
    """
    #Skipping initial 3 header and footer rows, and any columns that are unnamed (i.e. column A)
    return pd.read_excel(file_path, sheet_name=sheet_name, skiprows= range(0,3), skipfooter=3,
                         usecols=lambda x: 'Unnamed' not in x)

def extract_group_and_date(file_path: str) -> dict[str,str]:
    """
    Reads through the file_path of the dataset and extracts the provider group and the date of the file.

    :param file_path: Takes the same input as the import_excel; input can be a local file path, or url.
                      Extraction uses the last part section of the string input to determine name.
    :return: A dictionary containing 2 keys: provider_group_name and date
    """
    result = {}
    # URLs are encoded, so you may see %20, indicating spaces. This line works for both urls and file paths.
    full_file_name = os.path.basename(file_path).replace('%20', ' ').replace('.xlsx', '')

    # Date will be in MMDDYY format, at the final 6 chars of file name.
    file_date = full_file_name[-6:]

    # Final format will be MM-DD-YYYY
    file_date = datetime.datetime.strptime(file_date, '%m%d%y').strftime('%m-%d-%Y')

    # Remove file extension, date component [:-6], and leading/trailing whitespaces
    result['provider_group_name']= full_file_name.replace('.xlsx', '')[:-6].strip()
    result['file_date'] = file_date

    return result

def load_df_to_db(df: pd.DataFrame, sql_server_name: str, target_db_name: str,
                  target_table: str, target_schema: str) -> None:
    '''
    Loads a data frame into a SQL table using a sql alchemy connection/engine.
    Note - this function will fail if table already exists, but if the table does not exist,
           it will be created at runtime.
    :param df: The dataframe that will be loaded
    :param sql_server_name: Name of SQL server, example: 'DESKTOP-QB0RL6F\SQLEXPRESS'
    :param target_db_name: Name of the target database
    :param target_table: Name of the target table
    :param target_schema: Name of the target schema
    :return: Void return.
    '''

    # Setup the connection Engine
    engine = sqlalchemy.create_engine(f'mssql+pyodbc://{sql_server_name}/{target_db_name}?driver=SQL+Server')

    # chunksize set to a low number to ensure batch does reach max limit
    df.to_sql(target_table, engine, if_exists='fail', schema=target_schema, index=False, chunksize=25, method='multi')

if __name__ == "__main__":

    ### Question 1 ###
    url = 'https://github.com/mwez-priviahealth/data_engineering_assessment/raw/master/PythonTestQuestions/Privia%20Family%20Medicine%20113018.xlsx'

    df = import_excel(url, 'Sheet1')

    # Handle special characters and spaces within columns. Note: Only DOB col has special character, so hard coding the fix.
    df.columns = df.columns.str.replace(' ', '')
    df.rename(columns={'DOB[1]': 'DOB'}, inplace=True)

    # Selecting a subset of the greater dataframe for the response to Qts1
    demo_df = df.iloc[:,:7]

    # Extract file name and date from the path
    file_info = extract_group_and_date(url)

    # Adding provider group and file date columns
    demo_df['ProviderGroup'] = file_info['provider_group_name']
    demo_df['FileDate'] = file_info['file_date']

    # Using Anon function to apply the logic for when a Middle name exists, we only use the first letter initial.
    demo_df['MiddleName'] = demo_df['MiddleName'].apply(lambda mn: str(mn)[0] if pd.notnull(mn) else mn)

    # Converting Sex column to M/F flag
    demo_df['Sex'] = demo_df['Sex'].apply(lambda x: 'M' if int(x) == 0 else 'F')


    ### Question 2 ###

    # Only concerned with rows where risk has increased
    qnr_df_full = df.loc[df['RiskIncreasedFlag'] == 'Yes']

    # Only interested in Quarters and Risk data for this DF
    cols = ['ID', 'AttributedQ1', 'AttributedQ2', 'RiskQ1', 'RiskQ2']

    qnr_df = pd.wide_to_long(qnr_df_full[cols], stubnames=['Attributed', 'Risk'],
                             i=['ID'], j='Quarter', suffix='\w+') #\w+ regex allows for string suffix, default is numeric.

    qnr_df['FileDate'] = file_info['file_date']

    # Reset the index so ID and Quarter can be pulled out as 'normal' columns; this simplifies the to_sql loading.
    qnr_df.reset_index(inplace=True)


    ### Loading data into Database setting ###
    ## Change the below commands based on your environments connections, database names, etc.

    load_df_to_db(demo_df,sql_server_name= 'DESKTOP-QB0RL6F\SQLEXPRESS', target_db_name='Sandbox',
                  target_table='demographics', target_schema='dbo') # Using dbo by default

    load_df_to_db(qnr_df,sql_server_name= 'DESKTOP-QB0RL6F\SQLEXPRESS', target_db_name='Sandbox',
                  target_table='quarters_and_risk', target_schema='dbo')


#### Final Comments
'''
Using SQL Alchemy and Pandas to generate the tables provides some convenience, but does cause some issues in terms of 
table structure. Data types for columns may not be accurate and length/size may not be efficient; 
e.g. varchar columns are generated at MAX length. To address this, we can run a CREATE TABLE command either directly in
SQL (e.g. via SSMS) or set up a connection with a cursor and execute the CREATE TABLE command from within Python. From
there the dataframes could get loaded into pre-existing tables. See below for an example:
CREATE TABLE [{DatabaseName}].[dbo].[demographics](
	[ID] INT NULL,
	[FirstName] NVARCHAR(500) NULL,
	[MiddleName] NVARCHAR(500) NULL,
	[LastName] NVARCHAR(500) NULL,
	[DOB] DATE NULL,
	[Sex] NVARCHAR(10) NULL,
	[FavoriteColor] NVARCHAR(500) NULL,
	[ProviderGroup] NVARCHAR(500) NULL,
	[FileDate] DATE NULL
) 

In addition to this file, there is a test script that does some light unit testing of the functions defined
within this script.


My setup is as follows:
python --version --> 3.10.1
SQL Server 2019 Express

IDEs - Pycharm and SSMS

Thank you,
Vamshi
'''




