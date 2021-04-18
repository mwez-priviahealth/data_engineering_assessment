#code used to extract risk attribution data

import pandas as pd
import re

class attr_file_uploader:

    #Intialization
    def __init__(self, import_file_path, import_file_name, import_sheet_name):
        self.import_file_path = import_file_path
        self.import_file_name = import_file_name
        self.import_sheet_name = import_sheet_name

    def upload(self):
        fullpath = self.import_file_path + self.import_file_name

        # gather provider name and file date from file name
        file_no_ext = self.import_file_name.split(".", 1)
        file_no_ext = file_no_ext[0]
        file_provider_name = file_no_ext[:-7]
        file_date = file_no_ext[-7:]

        # read into dataframe
        idf = pd.read_excel(fullpath, sheet_name=self.import_sheet_name)

        # for production work, I would write code to auto check for rows and columns with no content
        # for time, I am explicitly calling out specific rows and columns
        # I wouldn't assume consitency outside of a test
        idf.drop(idf.index[0], inplace=True)
        idf.drop(idf.index[0], inplace=True)
        idf.drop(idf.columns[0], axis=1, inplace=True)

        # prepare the header, remove special characters from row with header names using REGEX
        # yes, I know the joke
        # say you have one problem and then you decide to use regex, now you have two problems

        new_header = idf.iloc[0]

        for index, value in enumerate(new_header):
            new_header[index] = re.sub('[^A-Za-z0-9]+', '', new_header[index])

        new_header[4] = 'DOB'  # if had time adjust regex to handle also
        idf = idf[1:]
        idf.columns = new_header

        # Add File Information
        idf['ProviderName'] = file_provider_name
        idf['FileDate'] = file_date

        return idf
