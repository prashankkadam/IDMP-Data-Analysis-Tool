# -*- coding:/ utf-8 -*-
"""
This piece of software is bound by The MIT License (MIT)
Copyright (c) 2019 Prashank Kadam
Code written by : Prashank Kadam
User name - ADM-PKA187
Email ID : prashank.kadam@maersktankers.com
Created on - Fri Aug  2 09:38:28 2019
version : 1.0
"""

# This file has the function that imports the excel sheet and performs some
# basic operations which will be required for our dash board. Note that tha
# further processing of the imported data will be done in process.py

# Importing the required libraries
import pandas as pd


# Defining the function that will import the excel sheet
def import_csv(path):

    # Reading the excel file based on the sheet number
    df = pd.read_csv(path)

    # returning the pre-processed dataframe
    return df
