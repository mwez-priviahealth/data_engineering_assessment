import pandas as pd
import re
import psycopg2
import openpyxl

def create_dataframe():
    file_name = 'Privia Family Medicine 113018.xlsx'
    data = pd.read_excel(file_name, header=3)
    data = data.dropna(subset=['First Name', 'Sex'])
    new_headers = []
    header = data.columns
    for name in header:
        new_name = re.sub(r"[^a-zA-Z0-9+\s+$]", '', name)
        print(new_name)
        new_name = new_name.upper()
        new_headers.append(new_name.replace(' ', '_'))
    data.columns = new_headers

    return data, file_name


#change the thing so it I used a pivot instead. make the dataframe its own function. Then pass it.
def import_demographics():
    data, file_name = create_dataframe()
    pivot_data = data
    pivot_data['SEX'] = pivot_data['SEX'].replace({0: 'M', 1: 'F'})
    pivot_data['MIDDLE_NAME'] = pivot_data['MIDDLE_NAME'].str[0]
    pivot_data['PROVIDER_GROUP'] = file_name[:-12]
    pivot_data['FILE_DATE'] = (file_name[-12:-5])
    print(data)
    pivot_data = pivot_data.pivot(index=None, columns='FILE_DATE' ,values=['ID','FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME' ,'DOB1', 'SEX' ,'FAVORITE_COLOR'])
    print(pivot_data)
    return pivot_data

def unpivot():
    data, file_name = create_dataframe()
    return 0


def main():
    import_demographics()

main()