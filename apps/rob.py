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
df_rob = proc.process_rob()

# Creating another dataframe which contains only those columns that need to be displayed in
# the data table
df_rob_tab = df_rob[['Vessel name', 'Segment', 'Owner',
                     'Last fuel date', 'HS HFO stock', 'LS HFO stock',
                     'HS MDO stock', 'LS MDO stock', 'Head owner', 'Re-del date',
                     'Rec HFO Nov', 'Rec HFO Dec', 'Stock Nov',
                     'Stock Dec']]

# Defining the columns layout for the rob data table
rob_columns = [{"name": ["", "Vessel name"], "id": "Vessel name"},
               {"name": ["", "Segment"], "id": "Segment"},
               {"name": ["", "Owner"], "id": "Owner"},
               {"name": ["", "ROB Date"], "id": "Last fuel date"},
               {"name": ["", "HS HFO stock"], "id": "HS HFO stock"},
               {"name": ["", "LS HFO stock"], "id": "LS HFO stock"},
               {"name": ["", "HS MDO stock"], "id": "HS MDO stock"},
               {"name": ["", "LS MDO stock"], "id": "LS MDO stock"},
               {"name": ["", "Head owner"], "id": "Head owner"},
               {"name": ["", "Re-del date"], "id": "Re-del date"},
               # {"name": ["Recommended HS HFO R.O.B[Tons]", "1st Oct (1 Month stock)"], "id": "Rec HFO Oct"},
               # {"name": ["Recommended HS HFO R.O.B[Tons]", "1st Nov (20days stock)"], "id": "Rec HFO Nov"},
               {"name": ["Recommended HS HFO R.O.B[Tons]", "1st Dec (15days stock)"], "id": "Rec HFO Dec"},
               # {"name": ["Current Stock Vs. Recommended R.O.B[Tons]", "1st Oct ROB"], "id": "Stock Oct"},
               # {"name": ["Current Stock Vs. Recommended R.O.B[Tons]", "1st Nov ROB"], "id": "Stock Nov"},
               {"name": ["Current Stock Vs. Recommended R.O.B[Tons]", "1st Dec ROB"], "id": "Stock Dec"}]

df_rob_tank = df_rob[['Vessel name', 'Segment', 'Owner', 'Tank1', 'Cleaned1', 'Tank2', 'Cleaned2',
                      'Tank3', 'Cleaned3', 'Tank4', 'Cleaned4', 'Tank5', 'Cleaned5', 'SttTank1', 'SttCleaned1',
                      'SttTank2', 'SttCleaned2', 'SerTank1', 'SerCleaned1', 'SerTank2', 'SerCleaned2', 'SerTank3',
                      'SerCleaned3']]

tank_columns = [{"name": ["", "Vessel name"], "id": "Vessel name"},
                {"name": ["", "Segment"], "id": "Segment"},
                {"name": ["", "Owner"], "id": "Owner"},
                {"name": ["Bunker Tank Capacities (Red - Uncleaned, Green - Cleaned)", "Tank 1"], "id": "Tank1"},
                # {"name": ["Bunker Tank Capacities", "Tank 1"], "id": "Cleaned1"},
                {"name": ["Bunker Tank Capacities (Red - Uncleaned, Green - Cleaned)", "Tank 2"], "id": "Tank2"},
                # {"name": ["Bunker Tank Capacities", "Tank 2"], "id": "Cleaned2"},
                {"name": ["Bunker Tank Capacities (Red - Uncleaned, Green - Cleaned)", "Tank 3"], "id": "Tank3"},
                # {"name": ["Bunker Tank Capacities", "Tank 3"], "id": "Cleaned3"},
                {"name": ["Bunker Tank Capacities (Red - Uncleaned, Green - Cleaned)", "Tank 4"], "id": "Tank4"},
                # {"name": ["Bunker Tank Capacities", "Tank 4"], "id": "Cleaned4"},
                {"name": ["Bunker Tank Capacities (Red - Uncleaned, Green - Cleaned)", "Tank 5"], "id": "Tank5"},
                # {"name": ["Bunker Tank Capacities", "Tank 5"], "id": "Cleaned5"},
                {"name": ["Settling Tank (Red - Uncleaned, Green - Cleaned)", "Tank 1"], "id": "SttTank1"},
                # {"name": ["Settling Tank", "Tank 1"], "id": "SttCleaned1"},
                {"name": ["Settling Tank (Red - Uncleaned, Green - Cleaned)", "Tank 2"], "id": "SttTank2"},
                # {"name": ["Settling Tank", "Tank 2"], "id": "SttCleaned2"},
                {"name": ["Service Tank (Red - Uncleaned, Green - Cleaned)", "Tank 1"], "id": "SerTank1"},
                # {"name": ["Service Tank", "Tank 1"], "id": "SerCleaned1"},
                {"name": ["Service Tank (Red - Uncleaned, Green - Cleaned)", "Tank 2"], "id": "SerTank2"},
                # {"name": ["Service Tank", "Tank 2"], "id": "SerCleaned2"},
                {"name": ["Service Tank (Red - Uncleaned, Green - Cleaned)", "Tank 3"], "id": "SerTank3"},
                # {"name": ["Service Tank", "Tank 3"], "id": "SerCleaned3"}
                ]

# Creating a dataframe for stock table
df_stock_tab_rob = df_rob[['Vessel name', 'Segment', 'Last fuel date', 'HS HFO stock', 'Rec HFO Oct',
                           'Rec HFO Nov', 'Stock Oct', 'Stock Nov', 'Burn Oct', 'Burn Nov', 'Ops Comment']]

df_stock_tab_rob = df_stock_tab_rob.sort_values(by='Burn Oct', ascending=False)

# Naming the columns for the stock table
stock_columns_rob = [{"name": ["", "Vessel name"], "id": "Vessel name"},
                     {"name": ["", "Segment"], "id": "Segment"},
                     {"name": ["", "ROB Date"], "id": "Last fuel date"},
                     {"name": ["", "HS HFO[tons]"], "id": "HS HFO stock"},
                     # {"name": ["Recommended HS HFO R.O.B  [Tons]", "By 1st Oct(1 Months Stock)"], "id": "Rec HFO Oct"},
                     # {"name": ["Recommended HS HFO R.O.B  [Tons]", "By 1st Nov(20days Stock)"], "id": "Rec HFO Nov"},
                     {"name": ["Recommended HS HFO R.O.B  [Tons]", "By 1st Dec(15days Stock)"], "id": "Rec HFO Dec"},
                     # {"name": ["Current Stock  Vs.  Recommended R.O.B  [Tons]", "For 1st Oct ROB"], "id": "Stock Oct"},
                     # {"name": ["Current Stock  Vs.  Recommended R.O.B  [Tons]", "For 1st Nov ROB"], "id": "Stock Nov"},
                     {"name": ["Current Stock  Vs.  Recommended R.O.B  [Tons]", "For 1st Dec ROB"], "id": "Stock Dec"},
                     # {"name": ["Amount to be burned to reach safe ROB level", "For 1st Oct ROB"], "id": "Burn Oct"},
                     # {"name": ["Amount to be burned to reach safe ROB level", "For 1st Nov ROB"], "id": "Burn Nov"},
                     {"name": ["Amount to be burned to reach safe ROB level", "For 1st Dec ROB"], "id": "Burn Dec"},
                     {"name": ["", "Operator's Comment"], "id": "Ops Comment"}]

# Deleting duplicate entries based on vessel names:
df_rob = df_rob.drop_duplicates(subset='Vessel name')

# Defining the layout for the content in the Tabs
# Tab 1 layout:
tab1_content = dbc.Card(
    dbc.CardBody([
        # Displaying the data table for ROB consumption
        ly.disp_table(tab_id='datatable-rob', dataframe=df_rob_tab, columns=rob_columns)
    ]),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("ROB Plot", className="card-text", style={'font-weight': 'bold', 'font-size': '20px',
                                                             'color': 'grey'}),

            # Displaying the graph for ROB consumption for multiple fuel types
            ly.disp_graph_multi(name=['HS HFO', 'LS HFO', 'HS MDO ', 'LS MDO'],
                                x=df_rob['Vessel name'],
                                y=[df_rob['HS HFO stock'], df_rob['LS HFO stock'],
                                   df_rob['HS MDO stock'], df_rob['LS MDO stock']]),
            dbc.Button('Resize Graph', id='resize_rob', outline=True, color="info", className="mr-1"),
        ]
    ),
    className="mt-3",
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            # Displaying the data table for ROB consumption
            ly.disp_table(tab_id='datatable-rob-tank', dataframe=df_rob_tank, columns=tank_columns)
        ]
    ),
    className="mt-3",
)

# Tab 4 layout:
tab4_content = dbc.Card(
    dbc.CardBody(
        [
            # html.P("Table", className="card-text"),

            # Displaying the data table for monthly consumption
            ly.disp_table(tab_id='datatable-stock-rob', dataframe=df_stock_tab_rob, columns=stock_columns_rob)
        ]
    ),
    className="mt-3",
)

# Fetching the filter layout from the predefined layout for page filters
filter_monthly = html.Div([
    filters.get_filters(df_rob)
], style={'padding-bottom': '20px'})

layout = [
    # Declaring the monthly filter in the layout
    filter_monthly,

    # Declaring the tabs in the layout
    html.Div([dbc.Tabs(
        [
            dbc.Tab(tab1_content, id='tab_rob_1', label="Data Table",
                    label_style={'font-weight': 'bold', 'font-size': '20px', 'color': 'grey'}),
            dbc.Tab(tab2_content, id='tab_rob_2', label="Current ROB Plot",
                    label_style={'font-weight': 'bold', 'font-size': '20px', 'color': 'grey'}),
            dbc.Tab(tab3_content, id='tab_rob_3', label="Tank Capacity",
                    label_style={'font-weight': 'bold', 'font-size': '20px', 'color': 'grey'}),
            dbc.Tab(tab4_content, id='tab_rob_4', label="Target Vessels",
                    label_style={'font-weight': 'bold', 'font-size': '20px', 'color': 'grey'}),
        ]
    )
    ])
]
