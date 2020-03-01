# -*- coding:/ utf-8 -*-
"""
This piece of software is bound by The MIT License (MIT)
Copyright (c) 2019 Prashank Kadam
Code written by : Prashank Kadam
User name - ADM-PKA187
Email ID : prashank.kadam@maersktankers.com
Created on - Mon Aug 19 08:52:30 2019
version : 1.0
"""
# Importing the required libraries
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


# This file defines the layout for different display structures on the dashboard. Its has the detailed
# format of various figures present on the dashboard

# Function to display the layout and formatting of the data tables present in the dash app
def disp_table(tab_id, dataframe):
    return dash_table.DataTable(
        id=tab_id,
        # columns=columns,
        columns=[{"name": i, "id": i} for i in dataframe.columns],
        data=dataframe.to_dict('records'),
        page_current=0,
        page_size=20,
        page_action='custom',

        sort_action='custom',
        sort_mode='single',
        sort_by=[],

        # style_data_conditional=[
        #     {'if': {'row_index': 'odd'},
        #      'backgroundColor': 'rgb(248, 248, 248)'},
        #     {'if': {
        #         'column_id': 'Vessel name',
        #         'filter_query': '{Vessel name} eq "Maersk Piper (Scrubber)"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'Vessel name',
        #         'filter_query': '{Vessel name} eq "Songa Diamond (Scrubber)"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'Vessel name',
        #         'filter_query': '{Vessel name} eq "Songa Opal (Scrubber)"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'Vessel name',
        #         'filter_query': '{Vessel name} eq "Songa Topaz (Scrubber)"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'Vessel name',
        #         'filter_query': '{Vessel name} eq "Proteus (Scrubber)"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'Vessel name',
        #         'filter_query': '{Vessel name} eq "Pro Onyx (Scrubber)"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'Vessel name',
        #         'filter_query': '{Vessel name} eq "Stamatia (Scrubber)"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'Vessel name',
        #         'filter_query': '{Vessel name} eq "Eco Marina del ray (Scrubber)"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'Vessel name',
        #         'filter_query': '{Vessel name} eq "Castor (Scrubber)"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'Vessel name',
        #         'filter_query': '{Vessel name} eq "Ion M (Scrubber)"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {'column_id': 'HFO Avg'},
        #      'backgroundColor': '#F0B27A'},
        #     {'if': {'column_id': 'HFO BA'},
        #      'backgroundColor': '#F8C471'},
        #     {'if': {
        #         'column_id': 'Stock Oct',
        #         'filter_query': '{Stock Oct} eq "Okay"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'Stock Oct',
        #         'filter_query': '{Stock Oct} eq "High Stock"'},
        #         'backgroundColor': '#F08080'},
        #     {'if': {
        #         'column_id': 'Stock Nov',
        #         'filter_query': '{Stock Nov} eq "Okay"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'Stock Nov',
        #         'filter_query': '{Stock Nov} eq "High Stock"'},
        #         'backgroundColor': '#F08080'},
        #     {'if': {
        #         'column_id': 'Stock Dec',
        #         'filter_query': '{Stock Dec} eq "Okay"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'Stock Dec',
        #         'filter_query': '{Stock Dec} eq "High Stock"'},
        #         'backgroundColor': '#F08080'},
        #     {'if': {
        #         'column_id': 'Burn Oct',
        #         'filter_query': '{Burn Oct} eq "Safe"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'Burn Nov',
        #         'filter_query': '{Burn Nov} eq "Safe"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'Burn Dec',
        #         'filter_query': '{Burn Dec} eq "Safe"'},
        #         'backgroundColor': '#A6D785'},
        #
        #     #################################################################################
        #     {'if': {
        #         'column_id': 'Tank1',
        #         'filter_query': '{Cleaned1} eq "Yes"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'Tank1',
        #         'filter_query': '{Cleaned1} eq "No"'},
        #         'backgroundColor': '#F08080'},
        #     {'if': {
        #         'column_id': 'Tank2',
        #         'filter_query': '{Cleaned2} eq "Yes"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'Tank2',
        #         'filter_query': '{Cleaned2} eq "No"'},
        #         'backgroundColor': '#F08080'},
        #     {'if': {
        #         'column_id': 'Tank3',
        #         'filter_query': '{Cleaned3} eq "Yes"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'Tank3',
        #         'filter_query': '{Cleaned3} eq "No"'},
        #         'backgroundColor': '#F08080'},
        #     {'if': {
        #         'column_id': 'Tank4',
        #         'filter_query': '{Cleaned4} eq "Yes"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'Tank4',
        #         'filter_query': '{Cleaned4} eq "No"'},
        #         'backgroundColor': '#F08080'},
        #     {'if': {
        #         'column_id': 'Tank5',
        #         'filter_query': '{Cleaned5} eq "Yes"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'Tank5',
        #         'filter_query': '{Cleaned5} eq "No"'},
        #         'backgroundColor': '#F08080'},
        #
        #     {'if': {
        #         'column_id': 'SttTank1',
        #         'filter_query': '{SttCleaned1} eq "Yes"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'SttTank1',
        #         'filter_query': '{SttCleaned1} eq "No"'},
        #         'backgroundColor': '#F08080'},
        #     {'if': {
        #         'column_id': 'SttTank2',
        #         'filter_query': '{SttCleaned2} eq "Yes"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'SttTank2',
        #         'filter_query': '{SttCleaned2} eq "No"'},
        #         'backgroundColor': '#F08080'},
        #
        #     {'if': {
        #         'column_id': 'SerTank1',
        #         'filter_query': '{SerCleaned1} eq "Yes"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'SerTank1',
        #         'filter_query': '{SerCleaned1} eq "No"'},
        #         'backgroundColor': '#F08080'},
        #     {'if': {
        #         'column_id': 'SerTank2',
        #         'filter_query': '{SerCleaned2} eq "Yes"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'SerTank2',
        #         'filter_query': '{SerCleaned2} eq "No"'},
        #         'backgroundColor': '#F08080'},
        #     {'if': {
        #         'column_id': 'SerTank3',
        #         'filter_query': '{SerCleaned3} eq "Yes"'},
        #         'backgroundColor': '#A6D785'},
        #     {'if': {
        #         'column_id': 'SerTank3',
        #         'filter_query': '{SerCleaned3} eq "No"'},
        #         'backgroundColor': '#F08080'},
        #     #################################################################################
        #
        #     {'height': '40px',
        #      'font-size': '18px'}
        # ],

        # style_cell_conditional=[
        #     {'if': {'column_id': 'Ops Comment'},
        #      'minWidth': '250px', 'width': '500px', 'maxWidth': '500px',
        #      'whiteSpace': 'normal'}
        # ],
        #
        # style_header={'backgroundColor': 'skyblue',
        #               'font-weight': 'bold',
        #               'font-size': '18px',
        #               'height': '40px',
        #               'textAlign': 'center'},
        #
        # style_header_conditional=[
        #     {'if': {
        #         'column_id': 'SttTank1'},
        #         'backgroundColor': '#73B1B7'},
        #     {'if': {
        #         'column_id': 'SttTank2'},
        #         'backgroundColor': '#73B1B7'}
        # ],
        #
        # merge_duplicate_headers=True,
        #
        # style_table={'overflowX': 'scroll'},

        # style_cell_conditional=[
        #     {'if': {'column_id': 'Re-del date'},
        #      'minWidth': '115px', 'width': '115px', 'maxWidth': '115px'}]

        # style_as_list_view=True
    )


# Function to display the layout and formatting of the single bar graph present in the dash app
def disp_graph_single(name1, name2, x, y1, y2, hover):
    return dcc.Graph(
        id='graph-2-tabs',
        figure={
            'data': [go.Bar(name=name1, x=x, y=y1, marker_color='#DF646B', hovertext=hover.fillna('').tolist()),
                     go.Bar(name=name2, x=x, y=y2, opacity=1, marker=dict(color='rgba(0,0,0,0)',
                                                                          line=dict(color='#A40A13', width=2)))],
            'layout': go.Layout(
                xaxis={'title': 'Vessel Name', 'autorange': True},
                yaxis={'title': 'Consumption[Tons]'},
                margin={'l': 80, 'b': 150, 't': 10, 'r': 80},
                height=800,
                width=2500,
                barmode='overlay',
                autosize=True,
                legend=dict(x=0, y=1, orientation='h'),
                hoverlabel=dict(namelength=30)
            )
        },
    )


# Function to display the layout and formatting of the multiple graph present in the dash app
def disp_graph_multi(name, x, y):
    return dcc.Graph(
        id='graph-rob-tabs',
        figure={
            'data': [go.Bar(name=name[0], x=x, y=y[0], marker_color='#DF646B'),
                     go.Bar(name=name[1], x=x, y=y[1], marker_color='#3D85C6'),
                     go.Bar(name=name[2], x=x, y=y[2], marker_color='#EBA760'),
                     go.Bar(name=name[3], x=x, y=y[3], marker_color='#6AA84F')],
            'layout': go.Layout(
                xaxis={'title': 'Vessel Name', 'autorange': True},
                yaxis={'title': 'Current ROB stock[Tons]'},
                margin={'l': 80, 'b': 150, 't': 10, 'r': 80},
                height=800,
                width=2500,
                autosize=True,
                legend=dict(x=0, y=1, orientation='h')
            )
        }
    )


# Function to display the layout and formatting of the individual monthly consumption graph
def disp_stacked_multi(name, x, y):
    return dcc.Graph(
        id='graph-monthly-tabs',
        figure={
            'data': [go.Bar(name=name[0], x=x, y=y[0], marker_color='#F8DFE1'),
                     go.Bar(name=name[1], x=x, y=y[1], marker_color='#F6D7D9'),
                     go.Bar(name=name[2], x=x, y=y[2], marker_color='#F4CDCF'),
                     go.Bar(name=name[3], x=x, y=y[3], marker_color='#F1C0C3'),
                     go.Bar(name=name[4], x=x, y=y[4], marker_color='#EEB0B4'),
                     go.Bar(name=name[5], x=x, y=y[5], marker_color='#EA9CA1'),
                     go.Bar(name=name[6], x=x, y=y[6], marker_color='#E58389'),
                     go.Bar(name=name[7], x=x, y=y[7], marker_color='#DF646B'),
                     go.Bar(name=name[8], x=x, y=y[8], marker_color='#D73D46'),
                     go.Bar(name=name[9], x=x, y=y[9], marker_color='#CD0C18'),
                     go.Bar(name=name[10], x=x, y=y[10], marker_color='#A40A13'),
                     go.Bar(name=name[11], x=x, y=y[11], marker_color='#83080F')
                     ],
            'layout': go.Layout(
                barmode='stack',
                xaxis={'title': 'Vessel Name', 'autorange': True},
                yaxis={'title': 'Consumption[Tons]'},
                margin={'l': 80, 'b': 150, 't': 10, 'r': 80},
                height=800,
                width=2500,
                autosize=True,
                legend=dict(x=0, y=1, orientation='h')
            )
        }
    )
