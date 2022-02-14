import pandas as pd
import pyodbc
import os
from datetime import datetime

"""
 Privia Health Python demo
 Note: The DDL for the Sql tables is in the script PythonDemo_ddl and needs to run first
"""


class DBConn:
    """Handle Database Connections
       Note: Can be enhanced to handle Parameters such as Server, DBType, UserId, Pwd etc.
    """
    def __init__(self, conn_string):
        self.conn_string = conn_string

    def connection(self):
        """Connect to the Database and return a connection object"""
        return pyodbc.connect(self.conn_string)


class TransformAndLoad:
    """ Transform ProviderGroup Dataframe and persist to Database"""

    def rename_df_columns(self, df):
        df.rename(columns={
            "ID": "Id"
            , "First Name": "FirstName"
            , "Middle Name": "MiddleName"
            , "Last Name": "LastName"
            , "DOB[1]": "DOB"
            , "Favorite Color": "FavoriteColor"
            , "Risk Increased Flag": "RiskIncreasedFlag"
            , "Attributed Q1": "AttributedQ1"
            , "Attributed Q2": "AttributedQ2"
            , "Risk Q1": "RiskQ1"
            , "Risk Q2 ": "RiskQ2"
        }, inplace=True)
        return df

    def demographics(self, dbconn, ddf, provider_grp, dt_on_file):
        """ Transform and Persist Demographics from Dataframe"""
        ddf['MiddleName'] = df['MiddleName'].str[0]  # Take first Initial of MiddleName
        ddf['Sex'] = df['Sex'].apply(lambda x: 'F' if (x == 0) else 'M')  # Set Sex to M/F
        ddf.fillna('', inplace=True)  # replace NaN values with NULL

        # Technote: this is the SLOW way to insert records as each row is a separate INSERT statement.
        # Use an ORM layer such as SQL Alchemy for more efficient Inserts.
        cursor = dbconn.cursor()
        # Iterate over each row in the filtered dataframe and execute an insert into the Database
        for index, row in ddf.iterrows():
            cursor.execute("INSERT INTO dbo.Demographics "
                           "( ProviderGroup"
                           ", DateOnFile"
                           ", Id"
                           ", FirstName"
                           ", MiddleName"
                           ", LastName"  
                           ", DOB"
                           ", Sex"
                           ", FavoriteColor"                     
                           ") "
                           "values(?,?,?,?,?,?,?,?,?)"
                           , provider_grp
                           , dt_on_file
                           , row.Id
                           , row.FirstName
                           , row.MiddleName
                           , row.LastName
                           , row.DOB
                           , row.Sex
                           , row.FavoriteColor)
        dbconn.commit()
        cursor.close()

    def quarters (self, dbconn, qdf, provider_grp, dt_on_file):
        """ Transform/Unpivot and Persist Quarters from Dataframe"""
        qdf.fillna('', inplace=True)  # replace NaN values with NULL
        qdf = qdf[qdf['RiskIncreasedFlag'] == 'Yes']  # Filter out Risks that have not increased between Quarters

        # Remove columns we don't need
        qdf = qdf.drop(['FirstName', 'MiddleName', 'LastName', 'DOB', 'Sex', 'FavoriteColor'], axis=1)
        df_unpivot = pd.wide_to_long(qdf, ["Attributed", "Risk"], i="Id", j="Quarter", suffix='(Q1|Q2)').reset_index()

        # Technote: this is the SLOW way to insert records as each row is a separate INSERT statement.
        # Use an ORM layer such as SQL Alchemy for more efficient Inserts.
        cursor = dbconn.cursor()
        # Iterate over each row in the filtered dataframe and execute an insert into the Database
        for index, row in df_unpivot.iterrows():
            cursor.execute("INSERT INTO dbo.Quarters "
                           "( DateOnFile"
                           ", Id"
                           ", Quarter"
                           ", Attributed"
                           ", Risk"
                           ") "
                           "values(?,?,?,?,?)"
                           , date_on_file
                           , row.Id
                           , row.Quarter
                           , row.Attributed
                           , row.Risk)

        dbconn.commit()
        cursor.close()


if __name__ == '__main__':

    try:
        print('Load Starting')
        # Parameters to run
        # TODO these parameters should  be parameterized or driven by an Environment variable/confi
        load_dir = 'C:\\Users\\david\\PycharmProjects\\\PriviaPythonDemo001\\'
        db_connection_string = "DRIVER={SQL Server};SERVER=DESKTOP-3NKEVRE;DATABASE=PersonDatabase;Trusted_Connection=yes;"

        sql_conn = DBConn(db_connection_string).connection()

        # Set the columns we want to read from the XL doc.
        xl_columns = ['ID'
                      , 'First Name'
                      , 'Middle Name'
                      , 'Last Name'
                      , 'DOB[1]'
                      , 'Sex'
                      , 'Favorite Color'
                      , 'Attributed Q1'
                      , 'Attributed Q2'
                      , 'Risk Q1'
                      , 'Risk Q2 '  # Note: this column has a space at the end of it's name.
                      , 'Risk Increased Flag']

        for xl_file in os.listdir(load_dir):
            if xl_file.endswith('.xlsx'):
                new_full_filename = load_dir + xl_file
                file_name_wo_extension = os.path.splitext(xl_file)[0]
                date_on_file = datetime.strptime(file_name_wo_extension[-6:], '%m%d%y').strftime('%m/%d/%Y')
                provider_group = file_name_wo_extension[:-7]
                df = pd.read_excel(new_full_filename, header=3, skipfooter=3, usecols=xl_columns)
                df = TransformAndLoad().rename_df_columns(df)
                TransformAndLoad().demographics(sql_conn, df, provider_group, date_on_file)
                TransformAndLoad().quarters(sql_conn, df, provider_group, date_on_file)
                print(provider_group + " : has loaded")

        print('Load Complete')

    except Exception as e:
        print(e)




