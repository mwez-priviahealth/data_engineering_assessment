import pandas as pd
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

#########################################################################################
######### 1. Import the 'Demongraphic' data section to a table in the database ##########
#########################################################################################

# Read Excel File
file = "Privia Family Medicine 113018.xlsx"
demo = pd.read_excel(file, header=3, usecols=[
                     1, 2, 3, 4, 5, 6, 7], skipfooter=3)

# Define the sql schema as necessary. Fields should not include spaces or special characters.
# Rename the column names and Remove the unnecessary spaces
try:
    # Formatted columns
    demo.rename(columns={"First Name": "FirstName",
                         "Middle Name": "MiddleName",
                         "Last Name": "LastName",
                         "DOB[1]": "DOB",
                         "Favorite Color": "FavoriteColor"}, inplace=True)
    # Remove "Unknown" value in the FavoriteColor column
    demo['FavoriteColor'] = demo['FavoriteColor'].str.replace('Unknown', '')

    # Extract only the first initial of the Middel name
    demo['MiddleName'] = demo['MiddleName'].str[0]

    # Converted the Sex value to M or F: M for 0 and F for 1
    demo['Sex'] = ['M' if x == 0 else 'F' for x in demo['Sex']]

    # Remove NA values to non-space
    demo.fillna('', inplace=True)

    print("Passed")
except:
    print("Error Occured")

# Include fields in the data table that indicate the date of the file and the provider group located in the filename.
try:
    # Get Provider name and add a new column
    f = file.split('.')[0].split(' ')
    provider = ' '.join(f[0:-1])
    demo['ProviderGroup'] = provider

    # Get file date and convert it to desired format and Add it to new column
    filedate = f[-1]
    # filedate = datetime.strptime(filedate, '%m%d%y').strftime('%m/%d/%Y')
    demo['FileDate'] = filedate

    print("Passed")
except:
    print("Error Occured")


#########################################################################################
##### 2. Transform and import the 'Quarters' and 'Risk' data into a separate table. #####
#########################################################################################

# Read Quarters and Risk columns from the excel 
quar_risk = pd.read_excel(file, header=3, usecols=[
                    1, 8, 9, 10, 11, 12], skipfooter=3)

try:
    # Rename columns without spaces
    quar_risk.columns = quar_risk.columns.str.replace(' ', '')

    # Filter to only include records in which the patients risk has increased.
    quar_risk = quar_risk[quar_risk['RiskIncreasedFlag'] == 'Yes']

    # Unpivot the Quarters and Risk table
    df_quarter = pd.melt(quar_risk, id_vars='ID', value_vars=['AttributedQ1','AttributedQ2'], var_name='Quarters', value_name='Attributed_Flag')
    df_risk = pd.melt(quar_risk, id_vars='ID', value_vars=['RiskQ1','RiskQ2'], var_name='Risk', value_name='Risk_Score')
    
    # Combine both Unpivot dataframes
    qr = pd.merge(df_quarter, df_risk, how="inner", on="ID")
    
    #Add filedate and drop the Risk column
    qr['FileDate'] = filedate
    qr = qr.drop(columns=['Risk'])

    print("Passed")
except:
    print("Error")



################## Create MYSQL database connection #################

try:
    mydb = mysql.connector.connect(
        host='localhost', user="root", password="password", database="PersonDatabase")

    mycursor = mydb.cursor()
    print("Passed")

# Raise Error if any connection problem
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Worng name and passward")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

# Verify the database created
mycursor.execute("Show databases")
for db in mycursor:
    print(db)

## Create Demographics Table ##
mycursor.execute(''' 
            
                CREATE TABLE Demographics
                
                    (ID int,
                    First_Name varchar(255),
                    Middel_Name varchar(255),
                    Last_Name varchar(255),
                    DOB date,
                    Sex varchar(1),
                    Favorite_Color varchar(255),
                    Provider_Group varchar(1000),
                    FileDate varchar(8))
                    
                ''')

#Convert the Demo dataframe into a list of tuples and Insert values
try:
    #Convert records to list for inserting
    demo_record = demo.values.tolist()

    demo_query = ''' INSERT INTO Demographics (ID, First_Name, Middel_Name, Last_Name, DOB, Sex, Favorite_Color, Provider_Group, FileDate)
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                '''
    mycursor.executemany(demo_query, demo_record)

    print("Insert Completed")

except:
    print("Error")

## Create the Risk table ##
mycursor.execute('''
                
                CREATE TABLE Quarter_Risk
                    (
                        ID int,
                        Quarters varchar(100),
                        Attributed_Flag varchar(5),
                        Risk_Score float,
                        FileDate varchar(8)
                    )
                ''')

# Insert Quarters and Risk data
try:
    qr_record = qr.values.tolist()
    # qr_record
    qr_query = ''' INSERT INTO Quarter_Risk (ID, Quarters, Attributed_Flag, Risk_Score, FileDate)
                values (%s,%s,%s,%s,%s)
                '''
    mycursor.executemany(qr_query, qr_record)

    print("Insert Completed")
except:
    print("Check Error")


# Commit and close db 
try:
    mydb.commit()
    mydb.close()
    print("Load Completed")
except:
    print("Error")