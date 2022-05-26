import pandas as pd
import xlrd
import pyodbc
import re
from datetime import datetime

# Read Excel File
file_path = "Privia Family Medicine 113018.xlsx"
wb = xlrd.open_workbook(file_path)
sheet = wb.sheet_by_index(0)

# Extract File Group and File Date
file_date = re.search(r'\d{2}\d{2}\d{2}', file_path).group()
##print(file_date)
file_group = file_path[:file_path.find(file_date)]
##print(file_group)

# Connect SQL Server Database
conn = pyodbc.connect('Driver={SQL Server};'
					  'Server=LAPTOP-IIJG8D9Q;'
					  'Database=PersonDatabase;')
cursor = conn.cursor()

# Create Schema and Table Patient.Demographics
try:
	cursor.execute('CREATE SCHEMA Patient')
	conn.commit()
	print("Schema Patient Successfully Created!")
except pyodbc.ProgrammingError as error:
	print(error)

create_query1 = '''
				CREATE TABLE Patient.Demographics (
					ID VARCHAR(255),
					First_Name VARCHAR(255),
					Middle_Name CHAR(1),
					Last_Name VARCHAR(255),
					DOB VARCHAR(10),
					Sex CHAR(1),
					Favorite_Color VARCHAR(255),
					File_Sender_Group VARCHAR(255),
					File_Receiving_Date VARCHAR(10)
				);
			   '''
try:
	cursor.execute(create_query1)
	conn.commit()
	print("Table Patient.Demographics Successfully Created!")
except pyodbc.ProgrammingError as error:
	print(error)

# Insert Data from Excel to Table Patient.Demographics
insert_query1 = '''
				INSERT INTO Patient.Demographics (
					ID,
					First_Name,
					Middle_Name,
					Last_Name,
					DOB,
					Sex,
					Favorite_Color,
					File_Sender_Group,
					File_Receiving_Date
				)
				VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
			   '''
try:
	for line in range(4, 104):
		if str(int(sheet.cell_value(line,6))) == '0': sex = "M"	
		else: sex = "F"
		cursor.execute(insert_query1, sheet.cell_value(line,1), sheet.cell_value(line,2), sheet.cell_value(line,3)[:1], sheet.cell_value(line,4), xlrd.xldate_as_datetime(sheet.cell_value(line,5), 0).date().isoformat(), sex, sheet.cell_value(line,7), file_group, file_date)
		conn.commit()
	print("Table Patient.Demographics Successfully Loaded!")
except pyodbc.ProgrammingError as error:
	print(error)


# Create Table Patient.Risk_Patients
create_query2 = '''
				CREATE TABLE Patient.Risk_Patients (
					ID VARCHAR(255),
					Quarter CHAR(2),
					Attributed_Flag VARCHAR(3),
					RISK_SCORE float,
					File_Date VARCHAR(10)
				);
			   '''
try:
	cursor.execute(create_query2)
	conn.commit()
	print("Table Patient.Risk_Patients Successfully Created!")
except pyodbc.ProgrammingError as error:
	print(error)

### tried to use melt function but failed, will do research later ###
##df = pd.DataFrame(pd.read_excel(file_path))
##table_unpivot = df.melt(id_vars='ID', var_name='Attributed Q1', value_name = 'Risk Q1')
##print (table_unpivot)
#####################################################################

# Insert Data from Excel to Table
insert_query1 = '''
				INSERT INTO Patient.Risk_Patients (
					ID,
					Quarter,
					Attributed_Flag,
					RISK_SCORE,
					File_Date
				)
				VALUES(?, ?, ?, ?, ?)
			   '''
try:
	for line in range(4, 104):
		if str(sheet.cell_value(line,12)) == 'Yes':
			cursor.execute(insert_query1, sheet.cell_value(line,1), 'Q1', sheet.cell_value(line,8), sheet.cell_value(line,10), file_date)
			cursor.execute(insert_query1, sheet.cell_value(line,1), 'Q2', sheet.cell_value(line,9), sheet.cell_value(line,11), file_date)
			conn.commit()
		else:
			continue
	print("Table Patient.Risk_Patients Successfully Loaded!")
except pyodbc.ProgrammingError as error:
	print(error)