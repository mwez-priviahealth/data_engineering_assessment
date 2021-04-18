# Appends curated data to SQL Server tables

class dataLoader:

    def load_demo_data(ddf):
        import pyodbc as py
        import pandas as pd

        cnxn = py.connect(
            r'Driver=SQL Server;Server=localhost\SQLEXPRESS;Database=PersonDatabase;Trusted_Connection=yes;')
        cursor = cnxn.cursor()

        for index, row in ddf.iterrows():
            cursor.execute(
                "INSERT INTO dbo.Demographics([PersonID],[FirstName],[MI],[LastName],[DOB],[Sex],[FavoriteColor],"
                "[ProviderName],[FileDate]) values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [row['ID'], row['FirstName'], row['MI'], row['LastName'], row['DOB'], row['Sex'], row['FavoriteColor'],
                row['ProviderName'], row['FileDate']])

        cnxn.commit()
        cursor.close()
        cnxn.close()

    def load_risk_data(rdf):
        print('')

