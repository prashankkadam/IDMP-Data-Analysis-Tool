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
def process_data(path):

    # Reading the csv file from the given path
    df_processed = pd.read_csv(path)

    return df_processed
