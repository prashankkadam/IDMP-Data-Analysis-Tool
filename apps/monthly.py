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

# This file contains the layout of the monthly consumption page

# Importing the processed data
df_monthly = proc.process_monthly()

# Dropping the duplicate entries based on vessel name
df_monthly = df_monthly.drop_duplicates(subset='Vessel name')

# Creating another dataframe which contains only those columns that need to be displayed in
# the data table
df_monthly_tab = df_monthly[['Vessel name', 'Segment', 'Owner', 'HFO Avg', 'HFO BA',
                             'HFO Jan', 'HFO Feb', 'HFO Mar', 'HFO Apr', 'HFO May', 'HFO Jun',
                             'HFO Jul', 'HFO Aug', 'HFO Sep', 'HFO Oct', 'HFO Nov', 'HFO Dec'
                             ]]

monthly_columns = [{"name": ["Vessel name"], "id": "Vessel name"},
                   {"name": ["Segment"], "id": "Segment"},
                   {"name": ["Owner"], "id": "Owner"},
                   {"name": ["HS HFO Avg"], "id": "HFO Avg"},
                   {"name": ["HS HFO BA"], "id": "HFO BA"},
                   {"name": ["HS HFO Jan"], "id": "HFO Jan"},
                   {"name": ["HS HFO Feb"], "id": "HFO Feb"},
                   {"name": ["HS HFO Mar"], "id": "HFO Mar"},
                   {"name": ["HS HFO Apr"], "id": "HFO Apr"},
                   {"name": ["HS HFO May"], "id": "HFO May"},
                   {"name": ["HS HFO Jun"], "id": "HFO Jun"},
                   {"name": ["HS HFO Jul"], "id": "HFO Jul"},
                   {"name": ["HS HFO Aug"], "id": "HFO Aug"},
                   {"name": ["HS HFO Sep"], "id": "HFO Sep"},
                   {"name": ["HS HFO Oct"], "id": "HFO Oct"},
                   {"name": ["HS HFO Nov"], "id": "HFO Nov"},
                   {"name": ["HS HFO Dec"], "id": "HFO Dec"}]

# Creating a dataframe for stock table
df_stock_tab = df_monthly[['Vessel name', 'Segment', 'Last fuel date', 'HS HFO stock', 'Rec HFO Oct',
                           'Rec HFO Nov', 'Stock Oct', 'Stock Nov', 'Burn Oct', 'Burn Nov', 'Ops Comment']]

df_stock_tab = df_stock_tab.sort_values(by='Burn Oct', ascending=False)

# Naming the columns for the stock table
stock_columns = [{"name": ["", "Vessel name"], "id": "Vessel name"},
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

# Defining the layout for the content in the Tabs
# Tab 1 layout:
tab1_content = dbc.Card(
    dbc.CardBody(
        [
            # html.P("Table", className="card-text"),

            # Displaying the data table for monthly consumption
            ly.disp_table(tab_id='datatable-paging', dataframe=df_monthly_tab, columns=monthly_columns)
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("Current ROB vs Rec. ROB plot", className="card-text",
                   style={'font-weight': 'bold', 'font-size': '20px',
                          'color': 'grey'}),

            # Displaying the bar graph for average monthly HFO consumption
            ly.disp_graph_single(name1='Current HS HFO R.O.B.', name2='1st Dec Rec. HFO',
                                 x=df_monthly['Vessel name'], y1=[df_monthly['HS HFO stock']],
                                 y2=[df_monthly['1_Nov_ROB']], hover=df_monthly['Ops Comment']),
            dbc.Button('Resize Graph', id='resize_monthly', outline=True, color="info", className="mr-1")
        ]
    ),
    className="mt-3",
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("Avg Monthly Cons plot (HS HFO)", className="card-text", style={'font-weight': 'bold',
                                                                                   'font-size': '20px',
                                                                                   'color': 'grey'}),

            # Displaying the bar graph for average monthly HFO consumption
            ly.disp_stacked_multi(name=['HFO Jan', 'HFO Feb', 'HFO Mar', 'HFO Apr', 'HFO May', 'HFO Jun',
                                        'HFO Jul', 'HFO Aug', 'HFO Sep', 'HFO Oct', 'HFO Nov', 'HFO Dec'],
                                  x=df_monthly['Vessel name'],
                                  y=[df_monthly['HFO Jan'], df_monthly['HFO Feb'],
                                     df_monthly['HFO Mar'], df_monthly['HFO Apr'],
                                     df_monthly['HFO May'], df_monthly['HFO Jun'],
                                     df_monthly['HFO Jul'], df_monthly['HFO Aug'],
                                     df_monthly['HFO Sep'], df_monthly['HFO Oct'],
                                     df_monthly['HFO Nov'], df_monthly['HFO Dec']
                                     ]),
            dbc.Button('Resize Graph', id='resize_monthly_ind', outline=True, color="info", className="mr-1")
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
            ly.disp_table(tab_id='datatable-stock', dataframe=df_stock_tab, columns=stock_columns)
        ]
    ),
    className="mt-3",
)

# Fetching the filter layout from the predefined layout for page filters
filter_monthly = html.Div([
    filters.get_filters(df_monthly)
], style={'padding-bottom': '20px'})

layout = [
    # Declaring the monthly filter in the layout
    filter_monthly,

    # Declaring the tabs in the layout
    html.Div([dbc.Tabs(
        [
            dbc.Tab(tab1_content, id='tab_mon_1', label="Data Table",
                    label_style={'font-weight': 'bold', 'font-size': '20px', 'color': 'grey'}),
            dbc.Tab(tab2_content, id='tab_mon_2', label="Current ROB vs Rec. ROB plot",
                    label_style={'font-weight': 'bold', 'font-size': '20px', 'color': 'grey'}),
            dbc.Tab(tab3_content, id='tab_mon_3', label="Avg Monthly Cons plot (HS HFO)",
                    label_style={'font-weight': 'bold', 'font-size': '20px', 'color': 'grey'}),
            dbc.Tab(tab4_content, id='tab_mon_4', label="Target Vessels",
                    label_style={'font-weight': 'bold', 'font-size': '20px', 'color': 'grey'}),
        ]
    )
    ])
]
