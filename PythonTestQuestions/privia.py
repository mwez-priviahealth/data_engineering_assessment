import os
import pandas as pd
import sqlalchemy as db
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.sql.schema import Column

#EXTRACT DATA

FILEPATH = '/Users/melissa/Desktop/data_engineering_assessment-master/PythonTestQuestions/Privia Family Medicine 113018.xlsx' #insert correct filepath

def extract():

	path, filename = os.path.split(FILEPATH)
	root, ext = os.path.splitext(filename)
	group = ' '.join(filename.split(' ')[:-1])
	filedate = root.rsplit(' ')[3]

	df = pd.read_excel(FILEPATH, usecols="B:M", skiprows=3)
	df = df[:-3]

	return(group, filedate, df);

#TRANSFORM DATA 

def transform():

	group, filedate, df = extract()

	df.columns = df.columns.str.lower().str.replace(' ', '')

	df.rename(columns={'dob[1]': 'dob'}, inplace=True)
	df['dob'] = pd.to_datetime(df.dob)

	df['middlename'] = df['middlename'].str[:1]

	df.insert(7, "providergroup", group)
	df.insert(8, "filedate", filedate)

	df['filedate'] = pd.to_datetime(filedate)
	df['filedate'] = df['filedate'].dt.strftime('%m/%d/%Y')
	df['sex'] = df['sex'].astype(str)
	df['sex'] = df['sex'].str.replace("0","M").str.replace("1","F").str[:1]

	dcols = df[['id', 'firstname', 'middlename', 'lastname', 'dob', 'sex', 'favoritecolor', 'providergroup', 'filedate']]

	demographics = dcols.copy()

	qcols = df[['id','attributedq1','attributedq2', 'riskq1', 'riskq2', 'riskincreasedflag','filedate']]
	quartersrisk =  qcols.copy()
	quartersrisk = quartersrisk.loc[quartersrisk['riskincreasedflag'] == 'Yes']

	return(demographics, quartersrisk);

#CONNECT TO DATABASE AND LOAD DATA

def load():
	
	demographics, quartersrisk = transform()

	Base = declarative_base()

	if __name__ == "__main__":
		db_string = "postgresql://postgres:passwor@localhost:5432/persondatabase"
		engine = create_engine(db_string)
		Base.metadata.create_all(engine)

	demographics.to_sql(name='demo', con=engine, if_exists='replace', index=False, 
	dtype={'id': INTEGER(),
		'firstname': VARCHAR(50),
		'middlename': VARCHAR(50),
		'lastname': VARCHAR(50),
		'dob': TIMESTAMP(),
		'sex': VARCHAR(50),
		'favoritecolor': VARCHAR(50),
		'providergroup': VARCHAR(50),
		'filedate': DATE()})	
	
	quartersrisk.to_sql(name='qrtrsk', con=engine, if_exists='replace', index=False,
	dtype={'id': INTEGER(),
		'attributedq1': VARCHAR(50),
		'attributedq2': VARCHAR(50),
		'riskq1':  Float(precision=15, asdecimal=True),
		'riskq2': Float(precision=15, asdecimal=True),
		'riskincreasedflag': VARCHAR(50),
		'filedate': DATE()})
	
	with engine.connect() as con:
		engine.execute('ALTER TABLE demo ADD PRIMARY KEY (id);')
		engine.execute('ALTER TABLE qrtrsk ADD PRIMARY KEY (id);')
	
	return(engine, Base, Base.metadata);

#TEST QUERY

def test():
	
	engine, Base, Base.metadata = load()

	demo = db.Table('demo', Base.metadata, autoload=True, autoload_with=engine)
	query1 = db.select([demo])
	#query1 = db.select([demo]).where(demo.columns.sex == 'F')
	ResultProxy1 = engine.execute(query1).fetchall()
	dfdemo = pd.DataFrame(ResultProxy1)
	dfdemo.columns = ResultProxy1[0].keys()

	print()
	print("Demographics Table Returned from Database: ")
	print(dfdemo.head())
	print()

	qrtrsk = db.Table('qrtrsk', Base.metadata, autoload=True, autoload_with=engine)
	query2 = db.select([qrtrsk])
	#query2 = db.select([qrtrsk]).where(qrtrsk.columns.attributedq1 == 'No')
	ResultProxy2 = engine.execute(query2).fetchall()
	dfqr= pd.DataFrame(ResultProxy2)
	dfqr.columns = ResultProxy2[0].keys()

	print("QuarterRisk Table Returned from Database: ")
	print(dfqr.head())

	print()
	# Run unit tests from testreport.py
	print("Starting Unit Tests")
	import testreport

	return();

def main():

	transform()
	load()
	test()

main();
