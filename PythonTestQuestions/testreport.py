import os
import pandas as pd
from tabulate import tabulate
import sqlalchemy as db
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

import mytest

# import the data quality checks
from datatest import check_for_nulls
from datatest import check_for_min_max
from datatest import check_for_valid_values
from datatest import check_for_duplicates
from datatest import run_data_quality_check

# connect to database

Base = declarative_base()
db_string = "postgresql://postgres:passwor@localhost:5432/persondatabase"
engine = create_engine(db_string)
Base.metadata.create_all(engine)

print("Connected to data warehouse")

results = []
tests = {key:value for key,value in mytest.__dict__.items() if key.startswith('test')}
for testname,test in tests.items():
    test['engine'] = engine
    results.append(run_data_quality_check(**test))

dfr = pd.DataFrame(results)
dfr.index+=1
dfr.columns = ['Test Name', 'Table','Column','Test Passed']
print(tabulate(dfr,headers='keys',tablefmt='psql'))

print("Disconnected from data warehouse")
