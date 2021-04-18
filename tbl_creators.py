
# Creates the table in SQL Server, if it doesn't already exist


class TableCreator:

    def __init__(self):
        print('') # yes this is hacky, I get an indent error if I don't, something to learn here

    @staticmethod
    def create_demo_table():
        import pyodbc

        cnxn = pyodbc.connect(r'Driver=SQL Server;Server=localhost\SQLEXPRESS;Database=PersonDatabase;'
                              r'Trusted_Connection=yes;')
        cursor = cnxn.cursor()
        cursor.execute('''
            IF (NOT EXISTS (SELECT * 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_SCHEMA = 'dbo' 
                    AND  TABLE_NAME = 'Demographics'))
                BEGIN
                    CREATE TABLE dbo.Demographics
                    (
                    PersonId varchar(10) NOT NULL,  --Named to Match Foreign Key in other Tables
                    FirstName nvarchar(15),
                    MI char(1),
                    LastName nvarchar(20),
                    DOB date,
                    Sex char(1),
                    FavoriteColor nvarchar(10),
                    ProviderName nvarchar(25),
                    FileDate varchar(20)
               
                    --create index, PersonId is really a foreign key, not sure I can make it unique
                    --two providers my provide information on the same person on different dates
                    --a combined key may make more sense, if I had more time, I would research this idea
                    ,INDEX Idx_Demographics_PersonId NONCLUSTERED (PersonId)
                    --create nonclustered index on likely to be queried fields
                    ,INDEX Idx_Demographics_LstNm_DOB NONCLUSTERED (LastName, DOB)
                    --in a real situation, I would verify how the data is used before creating indexes
                    ,INDEX Idx_Demographics_ProvNm NONCLUSTERED (ProviderName)
                )
                END
                   ''')

        cnxn.commit()
        cursor.close()
        cnxn.close()

    # Not required for this test, but in a real situation, I would need to create this method
    @staticmethod
    def create_risk_att_table():
        print('')