from time import time,ctime
engine = None
def run_data_quality_check(**options):
    print("*" * 50)
    testname = options.pop("testname")
    test = options.pop("test")
    print(f"Starting test {testname}")
    print(ctime(time()))
    start_time = time()
    status = test(**options)
    print(f"Finished test {testname}")
    print(ctime(time()))
    end_time = time()
    print("Duration : ", str(end_time - start_time))
    print(f"Test Passed {status}")
    options.pop("engine")
    print("Test Parameters")
    for key,value in options.items():
        print(f"{key} = {value}")
    print()
    print("*" * 50)
    return testname,options.get('table'),options.get('column'),status

#Check for nulls

def check_for_nulls(column,table,engine=engine):
    row_count = engine.execute(f'SELECT COUNT({column}) FROM "{table}" WHERE {column} IS NULL')
    return bool(row_count)

#Check for min max range

def check_for_min_max(column,table,minimum,maximum,engine=engine):
    row_count = engine.execute(f'SELECT count({column}) FROM "{table}" where  {column} < {minimum} or {column} > {maximum}')
    return bool(row_count)

#Check for any invalid entries

def check_for_valid_values(column, table, valid_values=None,engine=engine):
    result = engine.execute(f'SELECT distinct({column}) FROM "{table}"')
    actual_values = {x[0] for x in result}
    print(actual_values)
    status = [value in valid_values for value in actual_values]
    return all(status)

#Check for duplicate entries

def check_for_duplicates(column,table,engine=engine):
    row_count = engine.execute(f'SELECT count({column}) FROM "{table}" group by {column} having count({column}) > 1').scalar()
    print(row_count)
    return not bool(row_count)

