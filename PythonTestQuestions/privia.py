import os
import pandas as pd
import sqlalchemy as db
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint



############ EXTRACT DATA ############ 



fullpath = '/Users/melissa/Desktop/data_engineering_assessment-master/PythonTestQuestions/Privia Family Medicine 113018.xlsx' #insert correct filepath

path, filename = os.path.split(fullpath)
root, ext = os.path.splitext(filename)
group = ' '.join(filename.split(' ')[:-1])
filedate = root.rsplit(' ')[3]

df = pd.read_excel(fullpath, usecols="B:M", skiprows=3)
df = df[:-3]


############ TRANSFORM DATA ############ 



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



############ TABLE SCHEMA AND CONNECT TO DATABASE ############ 



Base = declarative_base()

class Demographics(Base):
    __tablename__ = 'demo'
    id = Column(Integer, primary_key=True, unique=True)
    firstname = Column(String(50))
    middlename = Column(String(50))
    lastname = Column(String(50))
    dob = Column(DateTime)
    sex = Column(String(50))
    favoritecolor = Column(String(50))
    providergroup = Column(String(50))
    filedate = Column(Date)

class QuarterRisk(Base):
    __tablename__ = 'qrtrsk'
    id = Column(Integer, primary_key=True, unique=True)
    attributedq1 = Column(String(50))
    attributedq2 = Column(String(50))
    riskq1 = Column(Integer)
    riskq2 = Column(Integer)
    riskincreasedflag = Column(String(50))
    filedate = Column(Date)

if __name__ == "__main__":
    db_string = "postgresql://postgres:passwor@localhost:5432/persondatabase"
    engine = create_engine(db_string)
    Base.metadata.create_all(engine)



############ LOAD DATA ############


demographics.to_sql(name='demo', con=engine, if_exists='replace', index=False)

quartersrisk.to_sql(name='qrtrsk', con=engine, if_exists='replace', index=False)



############ TEST QUERY ############ 



print("\n")


##Check for valid entries

demo = db.Table('demo', Base.metadata, autoload=True, autoload_with=engine)
query1 = db.select([demo])
#query1 = db.select([demo]).where(demo.columns.sex == 'F')
ResultProxy1 = engine.execute(query1).fetchall()
dfdemo = pd.DataFrame(ResultProxy1)
dfdemo.columns = ResultProxy1[0].keys()

print("Demographics Table Returned from Database: ")
print(dfdemo.head())

print("\n")


#Check for valid entries

qrtrsk = db.Table('qrtrsk', Base.metadata, autoload=True, autoload_with=engine)
query2 = db.select([qrtrsk])
#query2 = db.select([qrtrsk]).where(qrtrsk.columns.attributedq1 == 'No')
ResultProxy2 = engine.execute(query2).fetchall()
dfqr= pd.DataFrame(ResultProxy2)
dfqr.columns = ResultProxy2[0].keys()

print("QuarterRisk Table Returned from Database: ")
print(dfqr.head())

print("\n")

#Check for nulls

query3 = engine.execute('SELECT COUNT(id) FROM "demo" WHERE id IS NULL').scalar()
print(f"Number of Nulls in ID Column in Demographics Table: {query3}")


#Check for min max range

query4 = engine.execute('SELECT COUNT(riskq1) FROM "qrtrsk" WHERE riskq1 < 0 OR riskq1 > 1').scalar()
print(f"Number of Entries in RiskQ1 Column outside Min Max Range of 0-1 in QuarterRisk Table: {query4}")


#Check for duplicate entries

query5 = engine.execute('SELECT COUNT(id) FROM "demo" GROUP BY id HAVING COUNT(id) > 1').scalar()
print(f"Number of Duplicate Entries in ID Column in Demographics Table: {query5}")


#Check for nulls

query6 = engine.execute('SELECT COUNT(id) FROM "qrtrsk" WHERE id IS NULL').scalar()
print(f"Number of Nulls in ID Column in QuarterRisk Table: {query6}")


#Check for duplicate entries

query7 = engine.execute('SELECT COUNT(id) FROM "qrtrsk" GROUP BY id HAVING COUNT(id) > 1').scalar()
print(f"Number of Duplicate Entries in ID Colum in QuarterRisk Table: {query7}")

print("\n")


