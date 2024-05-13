#Import Required Modules
import configparser
import re
import os
import openpyxl
import pandas as pd
import numpy as np

def config_file():
    create_config()
    
#Check for excel file in folder and validate its format
def compare_excel_names_by_pattern(folder_path, pattern):

    regex_pattern = re.compile(pattern)

    excel_files = [file for file in os.listdir(folder_path) if file.endswith('.xlsx') or file.endswith('.xls')]

    for excel_file in excel_files:
        match = regex_pattern.match(excel_file)
        if match:
            return excel_file
        else:
            print(f"File '{excel_file}' does not match the pattern.")       #to be added to logfile
            
            
def create_config():
    config = configparser.ConfigParser()
    column_date = "date"

    
    folder_path = "C:/Users/D117157/Automation Tracker"
    pattern = r'\d{4}-\d{2}-\d{2}' 
    file = compare_excel_names_by_pattern(folder_path, pattern)

    df = pd.read_excel(file, skiprows=2)

    config['Source']= {
        'name': 'Aladdin',
        'source_file_name':file
    }

    config['Reception']= {
        'path': folder_path
    }

    config['Date'] = {
        'Date': df["Date"][0]
    }

    config['Frequency']= {
        'reception_freq': 'weekly'
    }

    config['Notification']= {
        'email_notification': 'true',
        'email_address': "deshpande.tanmay@paincipal.com"
    }

    Header = 'Header'
    header_name = ['Widget','Layout','Portfolio Full Name','Portfolio Short Name','Date','Currency','Benchmark','Look-through']
    
    config[Header] = {'header_name':','.join(header_name)}

    Column_data = 'Column'
    Column_name = ['Security Description','CUSIP','ISIN','Bloomberg Ticker','Price','PGI-Merrill Lynch Sector Breakdown (PGI_BAMLSECT) - Level 1','PGI-Merrill Lynch Sector Breakdown (PGI_BAMLSECT) - Level 2','PGI-Merrill Lynch Sector Breakdown (PGI_BAMLSECT) - Level 3','PGI-Merrill Lynch Sector Breakdown (PGI_BAMLSECT) - Level 4','PGI - Risk Country Bloc Summary (PGI_RISKCNTRY) - Level 1','PGI - Risk Country Bloc Summary (PGI_RISKCNTRY) - Level 2','Barclays Rating','S&P Rating',"Moody",'Fitch Rating','Yield to Maturity','Yield to Worst','OAS','Duration','Spread Duration']

    config[Column_data] = {'Column_name':','.join(Column_name)}

    Primary_cols = 'Primary_columns'
    primary_columns = ['Security Description','CUSIP','ISIN','Bloomberg Ticker','Message']

    config[Primary_cols] = {'primary_columns':','.join(primary_columns)}

    with open('config.ini','w') as configfile:
        config.write(configfile)
     
    return file, df

if __name__== "__main__":
    file, df = create_config()

    # Access the required data from Config File
    config = configparser.ConfigParser()
    config.read('config.ini')
    date = config.get('Date', 'Date')
    file_name = config.get('Source', 'source_file_name')
    freq = config.get('Frequency', 'reception_freq')
    path = config.get('Reception', 'path')
    header = config.get('Header', 'header_name').split(',')  # Access Header
    column_name = config.get('Column', 'column_name').split(',')  # Access Columns
    primary_columns = config.get('Primary_columns', 'primary_columns').split(',')

    # Your remaining code follows from here...
    # Ensure to integrate this part with the existing code
