To convert the provided code to use the `xlrd` module, we'll need to make several changes. `xlrd` is a library for reading data and formatting information from Excel files, unlike `openpyxl`, which is used for reading and writing Excel files. Here's the modified code:

```python
#Created by Shridhar and Tanmay
#Date 06/05/2024

#importing all the required libraries/modules
import numpy as np
import pandas as pd
import os
import re
import xlrd
from datetime import datetime
from Config import config_file
import configparser
import logging

if os.path.exists(os.path.join(os.getcwd(),"logs.log"))==True:
    os.remove('logs.log')
logging.basicConfig(filename='logs.log',format='%(asctime)s - %(message)s', level=logging.INFO)

config = configparser.ConfigParser()
logging.info('Writing Config.ini')
config_file()
logging.info('Created Config.ini succesfully')

# Python3 code to convert a tuple
# into a string using a for loop

#convert tuple into string

#Access the required data from Config File
config.read('config.ini')
date = config.get('Date','date')
file_name = config.get('Source','source_file_name')
freq = config.get('Frequency','reception_freq')
path = config.get('Reception','path')
header = config.get('Header','header_name').split(',')  #Access Header
column_name = config.get('Column','column_name').split(',') #Access Columns
primary_columns = config.get('Primary_columns','primary_columns').split(',')

workbook = xlrd.open_workbook(os.path.join(path, file_name))
worksheet = workbook.sheet_by_index(0)  # Assuming the first sheet is the one you want to work with

no_of_rows = worksheet.nrows - 1

# Function to move file from current location to the required folder
def move_file(file_name, to_foldername):
    current_dir = os.getcwd()
    new_dir = os.path.join(current_dir, to_foldername)
    if os.path.isfile(file_name):
        current_file_path = os.path.join(current_dir, file_name)
        new_file_path = os.path.join(new_dir, file_name)
        logging.info('Creating Folder' + new_dir)
        os.rename(current_file_path, new_file_path)

# Creation of Folders
def create_folder():
    if not os.path.exists(os.path.join(os.getcwd(), "Reception")):
        os.mkdir("Reception")

    if not os.path.exists(os.path.join(os.getcwd(), "Archive")):
        os.mkdir("Archive")
    
    if not os.path.exists(os.path.join(os.getcwd(), "Failure")):
        os.mkdir("Failure")

    if not os.path.exists(os.path.join(os.getcwd(), "Logs")):
        os.mkdir("Logs")

# Function to check the header name
def check_header_name(file_path, search_strings):
    logging.info('Fetching the header name')
    found_coordinates = []
    for row_index in range(worksheet.nrows):
        for col_index in range(worksheet.ncols):
            cell_value = str(worksheet.cell_value(row_index, col_index))
            if any(search_string in cell_value for search_string in search_strings):
                found_coordinates.append((row_index, col_index))
                if len(found_coordinates) == 8:
                    return found_coordinates

# Function to check the Column name
def search_columns_name_in_excel(file_path, search_strings):
    logging.info('Fetching the column name')
    column_coordinates = []
    for row_index in range(worksheet.nrows):
        for col_index in range(worksheet.ncols):
            cell_value = str(worksheet.cell_value(row_index, col_index))
            if any(search_string in cell_value for search_string in search_strings):
                column_coordinates.append((row_index, col_index))
                if len(column_coordinates) == 25:
                    return column_coordinates

col_coordinate = search_columns_name_in_excel(os.path.join(path, file_name), column_name)

# Function to validate the header
def validate_structure():
    coordinates = check_header_name(os.path.join(path, file_name), header)
    if len(coordinates) != 8:
        return False
    else:
        column_coordinates = search_columns_name_in_excel(os.path.join(path, file_name), column_name)
        if len(column_coordinates) != 20:
            return False
        else:
            return True

# Function to check File name with header names and Validate
def file_Validation():
    file_name_layout = worksheet.cell_value(0, 0)

    original_date = datetime.strptime(date,"%d-%b-%Y")
    formatted_date = original_date.strftime("%Y-%m-%d")
    create_folder()

    if formatted_date in file_name and file_name_layout in file_name:
        if os.path.getsize(os.path.join(path, file_name)) != 0 and validate_structure():
            print("non zero size file")
            # move_file(file_name,"/Archive")
        else:
            move_file(file_name,"/Failure")
    else:
        move_file(file_name,"Failure")
        print("File Name validation check failure")

try:
    file_Validation()
except AssertionError:
    logging.info('Error Occured during file validation')
    move_file(file_name,"/Failure")
    exit

failed = []
null_values = []
negative_values = []
names = ["NULL_VALUES","NEGATIVE_VALUES","DataType_Error"]

def check_null(col_coordinates):
    logging.info('Checking the null values')
    wb1 = xlrd.open_workbook(filename="logfile.xlsx")

    ws1 = wb1.sheet_by_name('NULL_VALUES')
    ws2 = wb1.sheet_by_name('NEGATIVE_VALUES')
    ws3 = wb1.sheet_by_name('DataType_Error')
    logging.info('checking for validation')

    for x in range(len(col_coordinates)):
        title = column_name[x]

        for i in range(col_coordinates[0][0] + 2, no_of_rows):
            var = worksheet.cell_value(col_coordinates[x][0], i)
            lst = []

            if var is None:
                logging.info('Checking for null values')
                message = f"{column_name[x]} is NULL"
                coord = xlrd.formula.cellname(i, col_coordinates[x][1])
                failed.append(coord)
                lst.extend([worksheet.cell_value(0, col_coordinates[x][1]), worksheet.cell_value(1, col_coordinates[x][1]), worksheet.cell_value(2, col_coordinates[x][1]), worksheet.cell_value(3, col_coordinates[x][1]), message])
                for j, val in enumerate(lst):
                    ws1.write(ws1.nrows, j, val)
                wb1.save(filename="logfile.xlsx")

            if title == "Price" and var is not None:
                if not isinstance(var,(int,float)):
                    logging.info('Checking for negative values')
                    message = f"{column_name[x]} AT COLUMN {col_coordinates[x][0] + 1}{i + 1} Wrong Data type Detected"
                    coord = xlrd.formula.cellname(i, col_coordinates[x][1])
                    negative_values.append(coord)
                    lst.extend([worksheet.cell_value(0, col_coordinates[x][1]), worksheet.cell_value(1, col_coordinates[x][1]), worksheet.cell_value(2, col_coordinates[x][1]), worksheet.cell_value(3, col_coordinates[x][1]), message])
                    for j, val in enumerate(lst):
                        ws3.write(ws3.nrows,

 j, val)
                    wb1.save(filename="logfile.xlsx")
                else:
                    if var < 0:
                        logging.info('Checking for negative values')
                        message = f"{column_name[x]} AT COLUMN {col_coordinates[x][0] + 1}{i + 1} is NEGATIVE"
                        coord = xlrd.formula.cellname(i, col_coordinates[x][1])
                        negative_values.append(coord)
                        lst.extend([worksheet.cell_value(0, col_coordinates[x][1]), worksheet.cell_value(1, col_coordinates[x][1]), worksheet.cell_value(2, col_coordinates[x][1]), worksheet.cell_value(3, col_coordinates[x][1]), message])
                        for j, val in enumerate(lst):
                            ws2.write(ws2.nrows, j, val)
                        wb1.save(filename="logfile.xlsx")

            if "Sector Breakdown" in title and not isinstance(var, str):
                logging.info('Checking for Data Type')
                message = f"{column_name[x]} AT COLUMN {col_coordinates[x][0] + 1}{i + 1} is NOT STRING"
                coord = xlrd.formula.cellname(i, col_coordinates[x][1])
                negative_values.append(coord)
                lst.extend([worksheet.cell_value(0, col_coordinates[x][1]), worksheet.cell_value(1, col_coordinates[x][1]), worksheet.cell_value(2, col_coordinates[x][1]), worksheet.cell_value(3, col_coordinates[x][1]), message])
                for j, val in enumerate(lst):
                    ws3.write(ws3.nrows, j, val)
                wb1.save(filename="logfile.xlsx")

            if "Risk Country" in title and not isinstance(var, str):
                logging.info('Checking for Data Type')
                message = f"{column_name[x]} AT COLUMN {col_coordinates[x][0] + 1}{i + 1} is NOT STRING"
                coord = xlrd.formula.cellname(i, col_coordinates[x][1])
                negative_values.append(coord)
                lst.extend([worksheet.cell_value(0, col_coordinates[x][1]), worksheet.cell_value(1, col_coordinates[x][1]), worksheet.cell_value(2, col_coordinates[x][1]), worksheet.cell_value(3, col_coordinates[x][1]), message])
                for j, val in enumerate(lst):
                    ws3.write(ws3.nrows, j, val)
                wb1.save(filename="logfile.xlsx")

logging.info('Done with the validation')
move_file(file_name,"/Archive")

current_file_name = os.path.join(path, "logfile.xlsx")
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

new_file_name = f"{current_time}_logfile.xlsx"

os.rename(current_file_name, new_file_name)

move_file(new_file_name, "/Logs")
logging.info('Error Occured while Checking Null')
``` 

This code should work similarly to the previous one, but it now uses `xlrd` to handle Excel files. Make sure you have `xlrd` installed (`pip install xlrd`) before running this code.
