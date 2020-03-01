# -*- coding:/ utf-8 -*-
"""
This piece of software is bound by The MIT License (MIT)
Copyright (c) 2019 Prashank Kadam
Code written by : Prashank Kadam
User name - ADM-PKA187
Email ID : prashank.kadam@maersktankers.com
Created on - Wed Aug  7 10:51:30 2019
version : 1.0
"""

# Importing the required libraries
import dash_html_components as html
import dash_bootstrap_components as dbc
from pre import process as proc
from layouts import filters
from layouts import layout as ly
from layouts import navs

# This file contains the layout of the ROB planning page

# Fetching the processed data file for ROB consumption details
df_data = proc.process_data(path="data/bcw.csv")

# Defining the layout for the content in the Tabs
# Tab 1 layout:
tab1_content = dbc.Card(
    dbc.CardBody([
        # Displaying the data table for ROB consumption
        ly.disp_table(tab_id='datatable', dataframe=df_data)
    ]),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
        ]
    ),
    className="mt-3",
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
        ]
    ),
    className="mt-3",
)

layout = [
    # Declaring the tabs in the layout
    html.Div([dbc.Tabs(
        [
            dbc.Tab(tab1_content, id='tab_rob_1', label="Data Table",
                    label_style={'font-weight': 'bold', 'font-size': '20px', 'color': 'grey'}),
            dbc.Tab(tab2_content, id='tab_rob_2', label="Plot",
                    label_style={'font-weight': 'bold', 'font-size': '20px', 'color': 'grey'}),
            dbc.Tab(tab3_content, id='tab_rob_3', label="Quantization",
                    label_style={'font-weight': 'bold', 'font-size': '20px', 'color': 'grey'}),
        ]
    )
    ])
]
