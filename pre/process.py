# -*- coding:/ utf-8 -*-
"""
Created on Tue Jul 23 12:07:20 2019
This piece of software is bound by The MIT License (MIT)
Copyright (c) 2019 Prashank Kadam
Code written by : Prashank Kadam
User name - ADM-PKA187
Email ID : prashank.kadam@maersktankers.com
Created on - Wed Aug  7 09:19:04 2019
version : 1.0
"""
# This file processes the imported data and makes it ready to be displayed

# Importing the required libraries
from pre import import_data as imp
import pandas as pd
import numpy as np


# In this file, we process the imported data for all our sheets (Monthly, ROB, Bunkers) by performing the
# following operations:
# 1- Dropping the empty columns
# 2- Rename the columns
# 3- Indexing
# 4- Rounding the float variable to 2 decimal places

# Function for processing the data for the ROB planning page
def process_rob():
    # Fetching the ROB sheet for data merge
    # Setting the columns to be dropped from the ROB sheet
    drop_rob = ['Unnamed: 12', 'Unnamed: 17', 'Unnamed: 22',
                'Unnamed: 30', 'Unnamed: 34', 'Unnamed: 44',
                'Unnamed: 49', 'Unnamed: 53', 'Unnamed: 58',
                'Unnamed: 69', 'Unnamed: 74']

    # Setting the names of the renamed columns
    rob_columns = ['Operator', 'Segment', 'Owner', 'IMO', 'Vessel name', 'Head owner',
                   'Re-del date', 'Last fuel date', 'HS HFO stock', 'LS HFO stock',
                   'HS MDO stock', 'LS MDO stock', 'HS HFO', 'LS HFO', 'HS MDO', 'LS MDO',
                   'Op idle', 'Op disc', 'Op ballast', 'Op laden', 'Fuel op idle',
                   'Fuel op disc', 'Fuel op ballast', 'Fuel op laden', 'Fuel op cons', 'Fuel op act',
                   'Fuel op min', 'Non_ECA', 'ECA', 'Dock Scrub', 'Oct dec', ' Nov dec', 'Dec 30',
                   'Dec 15', 'Tanks', 'FO bunkers', 'FO setting', 'FO service', 'Tank filling',
                   'Rec HFO Oct', 'Rec HFO Nov', 'Rec HFO Dec', 'Rec HFO dec l15',
                   'Stock Oct', 'Stock Nov', 'Stock Dec', 'Burn Oct', 'Burn Nov',
                   'Burn Dec', 'Ops Comment', 'Tank1', 'Cleaned1', 'Tank2', 'Cleaned2', 'Tank3', 'Cleaned3',
                   'Tank4', 'Cleaned4', 'Tank5', 'Cleaned5', 'SttTank1', 'SttCleaned1', 'SttTank2',
                   'SttCleaned2', 'SerTank1', 'SerCleaned1', 'SerTank2', 'SerCleaned2', 'SerTank3', 'SerCleaned3']

    # Importing all the required data for the monthly rob sheet
    df_rob = imp.import_excel(path='data/IMO_2020.xlsx',
                              sheet='IMO _2020_Dont Edit',
                              skip_rows=2,
                              drop_columns=drop_rob,
                              renamed_columns=rob_columns)

    df_rob.dropna(subset=['Segment'], inplace=True)

    df_rob['Index'] = range(1, len(df_rob) + 1)

    df_rob = df_rob.round()

    # Correcting the data discrepancies present in the HS_HFO_stock column
    # df_rob['HS HFO stock'] = df_rob['HS HFO stock'].replace({' ': '0'})
    df_rob['HS HFO stock'] = df_rob['HS HFO stock'].fillna(0.0).astype(int)

    df_rob['Last fuel date'] = df_rob['Last fuel date'].dt.strftime('%d/%m/%Y')
    df_rob['Re-del date'] = df_rob['Re-del date'].dt.strftime('%d/%m/%Y')
    # df_rob['Last fuel date'] = df_rob['Last fuel date'].to_string()
    # df_rob[['Last fuel date', 'Last fuel time']] = df_rob['Last fuel date'].str.split('T')

    df_rob['Re-del date'] = df_rob['Re-del date'].apply(lambda x: x if x != 'NaT' else '')
    df_rob['Last fuel date'] = df_rob['Last fuel date'].apply(lambda x: x if x != 'NaT' else '')
    # df_rob['Burn Oct'] = df_rob['Burn Oct'].apply(lambda x: "%.f" % x if x != 'Safe' else 'Safe')
    # df_rob['Burn Nov'] = df_rob['Burn Nov'].apply(lambda x: "%.f" % x if x != 'Safe' else 'Safe')
    # df_rob['Burn Dec'] = df_rob['Burn Dec'].apply(lambda x: "%.f" % x if x != 'Safe' else 'Safe')

    df_processed = df_rob[['Index', 'Vessel name', 'Operator', 'Segment', 'Owner', 'IMO',
                           'Last fuel date', 'HS HFO stock', 'LS HFO stock',
                           'HS MDO stock', 'LS MDO stock', 'Head owner', 'Re-del date',
                           'Dock Scrub', 'Tanks', 'FO bunkers', 'FO setting', 'FO service',
                           'Tank filling', 'Rec HFO Oct', 'Rec HFO Nov', 'Rec HFO Dec',
                           'Stock Oct', 'Stock Nov', 'Stock Dec', 'Burn Oct', 'Burn Nov', 'Burn Dec',
                           'Ops Comment', 'Tank1', 'Cleaned1', 'Tank2', 'Cleaned2', 'Tank3',
                           'Cleaned3', 'Tank4', 'Cleaned4', 'Tank5', 'Cleaned5', 'SttTank1', 'SttCleaned1', 'SttTank2',
                           'SttCleaned2', 'SerTank1', 'SerCleaned1', 'SerTank2', 'SerCleaned2', 'SerTank3',
                           'SerCleaned3']]

    return df_processed


# Function for processing the data for the monthly consumption page
def process_monthly():
    # Fetching the ROB sheet for data merge
    # Setting the columns to be dropped from the ROB sheet
    drop_rob = ['Unnamed: 12', 'Unnamed: 17', 'Unnamed: 22',
                'Unnamed: 30', 'Unnamed: 34', 'Unnamed: 44',
                'Unnamed: 49', 'Unnamed: 53', 'Unnamed: 58',
                'Unnamed: 69', 'Unnamed: 74']

    # Setting the names of the renamed columns
    rob_columns = ['Operator', 'Segment', 'Owner', 'IMO', 'Vessel name', 'Head owner',
                   'Re-del date', 'Last fuel date', 'HS HFO stock', 'LS HFO stock',
                   'HS MDO stock', 'LS MDO stock', 'HS HFO', 'LS HFO', 'HS MDO', 'LS MDO',
                   'Op idle', 'Op disc', 'Op ballast', 'Op laden', 'Fuel op idle',
                   'Fuel op disc', 'Fuel op ballast', 'Fuel op laden', 'Fuel op cons', 'Fuel op act',
                   'Fuel op min', 'Non_ECA', 'ECA', 'Dock Scrub', 'Oct dec', ' Nov dec', 'Dec 30',
                   'Dec 15', 'Tanks', 'FO bunkers', 'FO setting', 'FO service', 'Tank filling',
                   'Rec HFO Oct', 'Rec HFO Nov', 'Rec HFO Dec', 'Rec HFO dec l15',
                   'Stock Oct', 'Stock Nov', 'Stock Dec', 'Burn Oct', 'Burn Nov',
                   'Burn Dec', 'Ops Comment', 'Tank1', 'Cleaned1', 'Tank2', 'Cleaned2', 'Tank3', 'Cleaned3',
                   'Tank4', 'Cleaned4', 'Tank5', 'Cleaned5', 'SttTank1', 'SttCleaned1', 'SttTank2',
                   'SttCleaned2', 'SerTank1', 'SerCleaned1', 'SerTank2', 'SerCleaned2', 'SerTank3', 'SerCleaned3']

    # Importing all the required data for the monthly rob sheet
    df_rob = imp.import_excel(path='data/IMO_2020.xlsx',
                              sheet='IMO _2020_Dont Edit',
                              skip_rows=2,
                              drop_columns=drop_rob,
                              renamed_columns=rob_columns)

    # Names of the columns to be dropped from the monthly excel sheet
    drop_monthly = ['Unnamed: 20']

    # Renamed columns for the monthly excel sheet
    monthly_columns = ['Operator', 'Segment', 'Owner', 'IMO', 'Vessel name', 'HFO Jan',
                       'HFO Feb', 'HFO Mar', 'HFO Apr', 'HFO May', 'HFO Jun',
                       'HFO Jul', 'HFO Aug', 'HFO Sep', 'HFO Oct', 'HFO Nov',
                       'HFO Dec', 'HFO Avg', 'HFO BA', '1_Nov_ROB', 'HH January', 'HL January',
                       'MH January', 'ML January', 'HH February', 'HL February', 'MH February',
                       'ML February', 'HH March', 'HL March', 'MH March', 'ML March',
                       'HH April', 'HL April', 'MH April', 'ML April', 'HH May',
                       'HL May', 'MH May', 'ML May', 'HH June', 'HL June',
                       'MH June', 'ML June', 'HH July', 'HL July', 'MH July',
                       'ML July', 'HH Aug', 'HL Aug', 'MH Aug', 'ML Aug', 'HH Sep', 'HL Sep',
                       'MH Sep', 'ML Sep', 'HH Oct', 'HL Oct', 'MH Oct', 'ML Oct', 'HH Nov',
                       'HL Nov', 'MH Nov', 'ML Nov', 'HH Dec', 'HL Dec', 'MH Dec', 'ML Dec']

    # Importing all the required data for the monthly excel sheet
    df_monthly = imp.import_excel(path='data/IMO_2020.xlsx',
                                  sheet='Monthly_Consumption _Trend',
                                  skip_rows=2,
                                  drop_columns=drop_monthly,
                                  renamed_columns=monthly_columns)

    df_rob_slice = df_rob[['Vessel name', 'Last fuel date', 'HS HFO stock', 'Dock Scrub', 'Tanks', 'Rec HFO Oct',
                           'Rec HFO Nov', 'Rec HFO Dec', 'Stock Oct', 'Stock Nov', 'Stock Dec', 'Burn Oct',
                           'Burn Nov', 'Burn Dec', 'Ops Comment']]

    df_monthly = pd.merge(df_monthly, df_rob_slice, on='Vessel name')

    # df_monthly = df_monthly.drop(df_monthly.index[160:181]).fillna(0)

    df_monthly.dropna(subset=['Segment'], inplace=True)

    df_monthly['Index'] = range(1, len(df_monthly) + 1)

    # Correcting the data discrepancies present in the HS_HFO_stock column
    # df_monthly['HS HFO stock'] = df_monthly['HS HFO stock'].replace({' ': '0'})
    df_monthly['HS HFO stock'] = df_monthly['HS HFO stock'].fillna(0.0).astype(int)

    df_monthly['Last fuel date'] = df_monthly['Last fuel date'].dt.strftime('%d/%m/%Y')

    df_rob['Last fuel date'] = df_rob['Last fuel date'].apply(lambda x: x if x != 'NaT' else '')

    df_monthly = df_monthly.round()

    # df_monthly['Burn Oct'] = df_monthly['Burn Oct'].apply(lambda x: "%.f" % x if x != 'Safe' else 'Safe')
    # df_monthly['Burn Nov'] = df_monthly['Burn Nov'].apply(lambda x: "%.f" % x if x != 'Safe' else 'Safe')
    # df_monthly['Burn Dec'] = df_monthly['Burn Dec'].apply(lambda x: "%.f" % x if x != 'Safe' else 'Safe')

    # Correcting the data discrepancies present in the HFO Jan column
    # df_monthly['HFO Jan'] = df_monthly['HFO Jan'].replace({' ': '0'})
    # df_monthly['HFO Jan'] = df_monthly['HFO Jan'].fillna(0.0).astype(int)

    df_processed = df_monthly[['Index', 'Vessel name', 'Operator', 'Segment', 'Owner', 'IMO', 'Last fuel date',
                               'HS HFO stock', 'HFO Avg', 'HFO BA', '1_Nov_ROB', 'HFO Jan', 'HFO Feb', 'HFO Mar',
                               'HFO Apr', 'HFO May', 'HFO Jun', 'HFO Jul', 'HFO Aug', 'HFO Sep', 'HFO Oct', 'HFO Nov',
                               'HFO Dec', 'Dock Scrub', 'Tanks', 'Rec HFO Oct', 'Rec HFO Nov',
                               'Rec HFO Dec', 'Stock Oct', 'Stock Nov', 'Stock Dec', 'Burn Oct', 'Burn Nov', 'Burn Dec',
                               'Ops Comment']]

    return df_processed
