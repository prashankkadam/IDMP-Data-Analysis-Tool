# -*- coding:/ utf-8 -*-
"""
This piece of software is bound by The MIT License (MIT)
Copyright (c) 2019 Prashank Kadam
Code written by : Prashank Kadam
User name - ADM-PKA187
Email ID : prashank.kadam@maersktankers.com
Created on - Fri Aug 16 17:28:51 2019
version : 1.0
"""
# Importing the required libraries
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd


# In this file we set the layout for the filters in the dash board, We are using a bootstrap container for the
# filters and using a row-wise allocation format to the drop-downs. There is also some custom CSS formatting for the
# container contents along with basic  pre-processing of the input data
def get_filters(dataframe):
    dataframe_owner = dataframe.sort_values(['Owner'])
    dataframe_vessel = dataframe.sort_values(['Vessel name'])
    dataframe_operator = dataframe.sort_values(['Operator'])
    dataframe_tanks = dataframe.sort_values(['Tanks'])

    filters = html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H5('Segment')],
                        style={'padding-left': '10px', 'padding-right': '10px', 'padding-bottom': '5px'}),

                    html.Div([
                        dcc.Dropdown(
                            id='dd_segment',
                            options=[{
                                'label': i,
                                'value': i
                            } for i in dataframe['Segment'].dropna().unique()],
                            multi=True
                        )],
                        style={'padding-left': '10px', 'padding-right': '10px', 'padding-bottom': '10px'})
                ]),
                dbc.Col([
                    html.Div([
                        html.H5('Owner')],
                        style={'padding-left': '10px', 'padding-right': '10px', 'padding-bottom': '5px'}),

                    html.Div([
                        dcc.Dropdown(
                            id='dd_owner',
                            options=[{
                                'label': i,
                                'value': i
                            } for i in dataframe_owner['Owner'].dropna().unique()],
                            multi=True
                        )],
                        style={'padding-left': '10px', 'padding-right': '10px', 'padding-bottom': '10px'})
                ]),
                dbc.Col([
                    html.Div([
                        html.H5('Vessel Name')],
                        style={'padding-left': '10px', 'padding-right': '10px', 'padding-bottom': '5px'}),

                    html.Div([
                        dcc.Dropdown(
                            id='dd_vessel',
                            options=[{
                                'label': i,
                                'value': i
                            } for i in dataframe_vessel['Vessel name'].dropna().unique()],
                            multi=True
                        )],
                        style={'padding-left': '10px', 'padding-right': '10px', 'padding-bottom': '10px'})
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H5('Operator')],
                        style={'padding-left': '10px', 'padding-right': '10px', 'padding-bottom': '5px'}),

                    html.Div([
                        dcc.Dropdown(
                            id='dd_operator',
                            options=[{
                                'label': i,
                                'value': i
                            } for i in dataframe_operator['Operator'].dropna().unique()],
                            multi=True
                        )],
                        style={'padding-left': '10px', 'padding-right': '10px'})
                ]),
                dbc.Col([
                    html.Div([
                        html.H5('Number of Tanks')],
                        style={'padding-left': '10px', 'padding-right': '10px', 'padding-bottom': '5px'}),

                    html.Div([
                        dcc.Dropdown(
                            id='dd_tanks',
                            options=[{
                                'label': i,
                                'value': i
                            } for i in dataframe_tanks['Tanks'].dropna().unique()],
                            multi=True
                        )],
                        style={'padding-left': '10px', 'padding-right': '10px'})
                ]),
                dbc.Col([
                    html.Div([
                        html.H5('Docking Period/Scrubber')],
                        style={'padding-left': '10px', 'padding-right': '10px', 'padding-bottom': '5px'}),

                    html.Div([
                        dcc.Dropdown(
                            id='dd_dock_scrub',
                            options=[{
                                'label': i,
                                'value': i
                            } for i in dataframe['Dock Scrub'].dropna().unique()],
                            multi=True
                        )],
                        style={'padding-left': '10px', 'padding-right': '10px'})
                ]),
            ])
        ])
    ])

    return filters


def process_filter(dataframe, value_vessel, value_segment, value_owner, value_operator, value_tanks, value_dock_scrub):
    # Setting a counter variable that can count the number of filters that have been added
    counter = 0

    # Creating temporary dataframes for each filter
    dfr1 = pd.DataFrame()
    dfr2 = pd.DataFrame()
    dfr3 = pd.DataFrame()
    dfr4 = pd.DataFrame()
    dfr5 = pd.DataFrame()
    dfr6 = pd.DataFrame()

    # Fetching the value of each filter separately from the master dataframe and assigning to
    # our temporary dataframes
    if value_vessel:
        dfr1 = dataframe.loc[dataframe['Vessel name'].isin(value_vessel)]
        counter += 1
    if value_segment:
        dfr2 = dataframe.loc[dataframe['Segment'].isin(value_segment)]
        counter += 1
    if value_owner:
        dfr3 = dataframe.loc[dataframe['Owner'].isin(value_owner)]
        counter += 1
    if value_operator:
        dfr4 = dataframe.loc[dataframe['Operator'].isin(value_operator)]
        counter += 1
    if value_tanks:
        dfr5 = dataframe.loc[dataframe['Tanks'].isin(value_tanks)]
        counter += 1
    if value_dock_scrub:
        dfr6 = dataframe.loc[dataframe['Dock Scrub'].isin(value_dock_scrub)]
        counter += 1

    # Merging all the dataframes into a list and concatenating them into a single dataframe
    frames = [dfr1, dfr2, dfr3, dfr4, dfr5, dfr6]
    dfr = pd.concat(frames)

    # If one or more of the filters have been selected, the couter will have a non-zero values
    # this value will correspond to the number of filters that have been applied
    # Using the counter value we will check how many time entries in our dataframe have repeated
    # equivalent to the counter value
    if counter != 0:
        dfr = dfr[dfr.groupby('Index')['Index'].transform('size') == counter]

    # If no filter has been selected, simply pass the whole  master dataframe as the output
    if not value_vessel and not value_segment and not value_owner and not value_operator and not value_tanks and \
            not value_dock_scrub:
        dfr = dataframe

    # Dropping duplicate entries that may have been added to due to filter selection criteria
    dfr = dfr.drop_duplicates()

    return dfr
