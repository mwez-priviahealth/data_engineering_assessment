
# Jeremy Hess Python Script for Privia Health 4/18/2021

# user defined packages
import fileUploaders as up
import extractors as de
import curators as dc
import tbl_creators as tc
import sqlDataLoaders as ld

file_path = r'C:\Users\hess_\Documents\\'
file_name = 'Privia Family Medicine 113018.xlsx'
sheet_name = 'Sheet1'

# This is where connection string information would go
# My instance of SQL Server on my laptop uses windows authentication, would not do that at work
# I would have the user enter connection info here and create a class that handles the connection info
# I will not build a generic connection handler here, but I would at work

# start by retrieving the attribution records, and store in a dataframe for easy manipulation
provDataUploader = up.attr_file_uploader(file_path, file_name, sheet_name)
prov_attr_raw = provDataUploader.upload()

# extract the demographic and risk score attribution data from the raw file
dataExtractor = de.AttrDemoDataExtract(prov_attr_raw)
ddf, qrdf = dataExtractor.extract()

# ddf is for demographic dataframe
# qrdf is for quarterly risk dataframe

# cleanse, curate and transpose the data as needed
provDataCurator = dc.DataCurator()
res_ddf = provDataCurator.curate_demographics(ddf)
res_qrdf = provDataCurator.curate_risk_attr(qrdf)

# In a work setting I would create a connector class
# I would bet "dollars to donuts" that you have this built already
# For expediency, I am just going to pass the connection string code as needed

# If it does not exist, create a table to hold data in sql server
sqlTableCreator = tc.TableCreator()
sqlTableCreator.create_demo_table()
sqlTableCreator.create_risk_att_table()
# doesn't actually make table, not required for test

# Insert records into respective SQL Server Table
sqlDemoDataLoader = ld.dataLoader()
sqlDemoDataLoader.load_demo_data(res_ddf)
# I would also do this for risk attr dataframe, not technically required for test
