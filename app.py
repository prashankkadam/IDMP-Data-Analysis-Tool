# -*- coding:/ utf-8 -*-
"""
This piece of software is bound by The MIT License (MIT)
Copyright (c) 2019 Prashank Kadam
Code written by : Prashank Kadam
User name - prashankkadam
Email ID : kadam.pr@husky.neu.edu
Created on - Wed Aug  7 10:51:30 2019
version : 1.0
"""
# Importing the required directories
import dash
import os
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from flask import Flask, render_template
from flask_basicauth import BasicAuth
from layouts import navs
from apps import rob, monthly, bunker
import pandas as pd
from pre import process as proc
import plotly.graph_objs as go
from layouts import filters

# This file initializes our app and sets external styling formats

# Creating a flask server
server = Flask(__name__)

# Hardcoding the basic auth user name and password
server.config['BASIC_AUTH_USERNAME'] = 'admin'
server.config['BASIC_AUTH_PASSWORD'] = 'mtimo2020'

# Creating the basic auth instance
basic_auth = BasicAuth(server)


# Routing the basic auth to html layout
@server.route('/secret')
@basic_auth.required
def secret_view():
    return render_template('secret.html')


# Assigning a key to the server
server.secret_key = os.environ.get('secret_key', 'secret')

server.config['BASIC_AUTH_FORCE'] = True

# Defining external stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Initializing the dash app
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app.config.suppress_callback_exceptions = True

# Initializing a server
# server = app.server

# Routing the static server path
# @app.server.route('/static/index.py')
# def static_file(path):
#    static_folder = os.path.join(os.getcwd(), 'static')
#   return send_from_directory(static_folder, path)

# Defining the basic layout of our dashboard (This will then be routed to the required pages)
app.layout = html.Div([
    navs.navbar,
    navs.nav,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Importing the ROB consumption data
df_rob = proc.process_rob()

# Importing the monthly consumption data
df_monthly = proc.process_monthly()


# Callback for the routing the URLs to the correct paths
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/rob':
        return rob.layout
    elif pathname == '/apps/monthly':
        return monthly.layout
    # elif pathname == '/apps/bunker':
    #     return bunker.layout
    else:
        return rob.layout


# Callback for data table on the ROB consumption page
@app.callback(
    Output('datatable-rob', 'data'),
    [Input('datatable-rob', "page_current"),
     Input('datatable-rob', "page_size"),
     Input('dd_vessel', "value"),
     Input('dd_segment', "value"),
     Input('dd_owner', "value"),
     Input('dd_operator', 'value'),
     Input('dd_tanks', 'value'),
     Input('dd_dock_scrub', 'value'),
     Input('datatable-rob', 'sort_by')])
def update_table_rob(page_current, page_size, value_vessel, value_segment, value_owner, value_operator,
                     value_tanks, value_dock_scrub, sort_by):
    # Fetching the filtered data:
    dfr_temp = filters.process_filter(df_rob, value_vessel, value_segment, value_owner, value_operator,
                                      value_tanks, value_dock_scrub)

    if len(sort_by):
        dfr = dfr_temp.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dfr = dfr_temp

    # Returning the filtered data to the table
    return dfr.iloc[
           : (page_current + 1) * page_size
           ].to_dict('records')
    # page_current * page_size


# Callback for the multiple bar graph on the ROB consumption URL
@app.callback(Output('graph-rob-tabs', "figure"),
              [Input('dd_vessel', "value"),
               Input('dd_segment', "value"),
               Input('dd_owner', "value"),
               Input('dd_operator', 'value'),
               Input('dd_tanks', 'value'),
               Input('dd_dock_scrub', 'value'),
               Input('resize_rob', 'n_clicks')])
def update_figure_rob(value_vessel, value_segment, value_owner, value_operator, value_tanks, value_dock_scrub,
                      n_clicks):
    # Fetching the filtered data:
    dfr = filters.process_filter(df_rob, value_vessel, value_segment, value_owner, value_operator,
                                 value_tanks, value_dock_scrub)
    dfr = dfr.drop_duplicates(subset='Vessel name')

    if n_clicks:
        return {
            'data': [go.Bar(name='HS HFO', x=dfr['Vessel name'], y=dfr['HS HFO stock'], marker_color='#DF646B'),
                     go.Bar(name='LS HFO', x=dfr['Vessel name'], y=dfr['LS HFO stock'], marker_color='#3D85C6'),
                     go.Bar(name='HS MDO', x=dfr['Vessel name'], y=dfr['HS MDO stock'], marker_color='#EBA760'),
                     go.Bar(name='LS MDO', x=dfr['Vessel name'], y=dfr['LS MDO stock'], marker_color='#6AA84F')],
            'layout': go.Layout(
                xaxis={'title': 'Vessel Name', 'autorange': True},
                yaxis={'title': 'Current ROB stock[Tons]'},
                margin={'l': 80, 'b': 150, 't': 10, 'r': 80},
                autosize=True,
                legend=dict(x=0, y=1, orientation='h')
            )
        }

    # Returning the filtered data to the graph
    return {
        'data': [go.Bar(name='HS HFO', x=dfr['Vessel name'], y=dfr['HS HFO stock'], marker_color='#DF646B'),
                 go.Bar(name='LS HFO', x=dfr['Vessel name'], y=dfr['LS HFO stock'], marker_color='#3D85C6'),
                 go.Bar(name='HS MDO', x=dfr['Vessel name'], y=dfr['HS MDO stock'], marker_color='#EBA760'),
                 go.Bar(name='LS MDO', x=dfr['Vessel name'], y=dfr['LS MDO stock'], marker_color='#6AA84F')],
        'layout': go.Layout(
            xaxis={'title': 'Vessel Name', 'autorange': True},
            yaxis={'title': 'Current ROB stock[Tons]'},
            margin={'l': 80, 'b': 150, 't': 10, 'r': 80},
            autosize=True,
            legend=dict(x=0, y=1, orientation='h')
        )
    }


# Callback for data table on the ROB tank capacity
@app.callback(
    Output('datatable-rob-tank', 'data'),
    [Input('datatable-rob-tank', "page_current"),
     Input('datatable-rob-tank', "page_size"),
     Input('dd_vessel', "value"),
     Input('dd_segment', "value"),
     Input('dd_owner', "value"),
     Input('dd_operator', 'value'),
     Input('dd_tanks', 'value'),
     Input('dd_dock_scrub', 'value'),
     Input('datatable-rob-tank', 'sort_by')])
def update_table_rob_tank(page_current, page_size, value_vessel, value_segment, value_owner, value_operator,
                          value_tanks, value_dock_scrub, sort_by):
    # Fetching the filtered data:
    dfr_temp = filters.process_filter(df_rob, value_vessel, value_segment, value_owner, value_operator,
                                      value_tanks, value_dock_scrub)

    if len(sort_by):
        dfr = dfr_temp.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dfr = dfr_temp

    # Returning the filtered data to the table
    return dfr.iloc[
           :(page_current + 1) * page_size
           ].to_dict('records')


# Callback for stock table on the rob consumption page
@app.callback(
    Output('datatable-stock-rob', 'data'),
    [Input('datatable-stock-rob', "page_current"),
     Input('datatable-stock-rob', "page_size"),
     Input('dd_vessel', "value"),
     Input('dd_segment', "value"),
     Input('dd_owner', "value"),
     Input('dd_operator', 'value'),
     Input('dd_tanks', 'value'),
     Input('dd_dock_scrub', 'value'),
     Input('datatable-stock-rob', 'sort_by')])
def update_stock_rob(page_current, page_size, value_vessel, value_segment, value_owner, value_operator,
                     value_tanks, value_dock_scrub, sort_by):
    # Fetching the filtered data:
    dfr_temp = filters.process_filter(df_rob, value_vessel, value_segment, value_owner, value_operator,
                                      value_tanks, value_dock_scrub)

    # Deleting duplicate entries:
    dfr_temp = dfr_temp.drop_duplicates(subset='Vessel name')

    dfr_temp = dfr_temp.sort_values(by='Burn Oct', ascending=False)

    if len(sort_by):
        dfr = dfr_temp.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dfr = dfr_temp

    # Returning the filtered data to the table
    return dfr.iloc[
           :(page_current + 1) * page_size
           ].to_dict('records')


# Callback for data table on the monthly consumption page
@app.callback(
    Output('datatable-paging', 'data'),
    [Input('datatable-paging', "page_current"),
     Input('datatable-paging', "page_size"),
     Input('dd_vessel', "value"),
     Input('dd_segment', "value"),
     Input('dd_owner', "value"),
     Input('dd_operator', 'value'),
     Input('dd_tanks', 'value'),
     Input('dd_dock_scrub', 'value'),
     Input('datatable-paging', 'sort_by')])
def update_table_monthly(page_current, page_size, value_vessel, value_segment, value_owner, value_operator,
                         value_tanks, value_dock_scrub, sort_by):
    # Fetching the filtered data:
    dff_temp = filters.process_filter(df_monthly, value_vessel, value_segment, value_owner, value_operator,
                                      value_tanks, value_dock_scrub)

    # Deleting duplicate entries:
    dff_temp = dff_temp.drop_duplicates(subset='Vessel name')

    if len(sort_by):
        dff = dff_temp.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = dff_temp

    # Returning the filtered data to the table
    return dff.iloc[
           :(page_current + 1) * page_size
           ].to_dict('records')


# Callback for the bar graph on the monthly consumption page
@app.callback(Output('graph-2-tabs', "figure"),
              [Input('dd_vessel', "value"),
               Input('dd_segment', "value"),
               Input('dd_owner', "value"),
               Input('dd_operator', 'value'),
               Input('dd_tanks', 'value'),
               Input('dd_dock_scrub', 'value'),
               Input('resize_monthly', 'n_clicks')])
def update_figure_monthly(value_vessel, value_segment, value_owner, value_operator, value_tanks, value_dock_scrub,
                          n_clicks):
    # Fetching the filtered data:
    dff = filters.process_filter(df_monthly, value_vessel, value_segment, value_owner, value_operator,
                                 value_tanks, value_dock_scrub)

    # Deleting duplicate entries:
    dff = dff.drop_duplicates(subset='Vessel name')

    if n_clicks:
        return {
            'data': [go.Bar(name='Current HS HFO R.O.B.', x=dff['Vessel name'], y=dff['HS HFO stock'],
                            marker_color='#DF646B', hovertext=dff["Ops Comment"].fillna('').tolist()),
                     go.Bar(name='1st Dec Rec. HFO', x=dff['Vessel name'], y=dff['1_Nov_ROB'], opacity=1,
                            marker=dict(color='rgba(0,0,0,0)', line=dict(color='#A40A13', width=2)))
                     ],
            'layout': go.Layout(
                xaxis={'title': 'Vessel Name', 'autorange': True},
                yaxis={'title': 'Consumption[Tons]'},
                margin={'l': 80, 'b': 150, 't': 10, 'r': 80},
                barmode='overlay',
                autosize=True,
                legend=dict(x=0, y=1, orientation='h'),
                hoverlabel=dict(namelength=30)
            )
        }

    # Returning the filtered data to the graph
    return {
        'data': [go.Bar(name='Current HS HFO R.O.B.', x=dff['Vessel name'], y=dff['HS HFO stock'],
                        marker_color='#DF646B', hovertext=dff["Ops Comment"].fillna('').tolist()),
                 go.Bar(name='1st Dec Rec. HFO', x=dff['Vessel name'], y=dff['1_Nov_ROB'], opacity=1,
                        marker=dict(color='rgba(0,0,0,0)', line=dict(color='#A40A13', width=2)))
                 ],
        'layout': go.Layout(
            xaxis={'title': 'Vessel Name', 'autorange': True},
            yaxis={'title': 'Consumption[Tons]'},
            margin={'l': 80, 'b': 150, 't': 10, 'r': 80},
            barmode='overlay',
            autosize=True,
            legend=dict(x=0, y=1, orientation='h'),
            hoverlabel=dict(namelength=30)
        )
    }


# Callback for the bar graph on individual monthly consumptions on the monthly consumption page
@app.callback(Output('graph-monthly-tabs', "figure"),
              [Input('dd_vessel', "value"),
               Input('dd_segment', "value"),
               Input('dd_owner', "value"),
               Input('dd_operator', 'value'),
               Input('dd_tanks', 'value'),
               Input('dd_dock_scrub', 'value'),
               Input('resize_monthly_ind', 'n_clicks')])
def update_values_monthly(value_vessel, value_segment, value_owner, value_operator, value_tanks, value_dock_scrub,
                          n_clicks):
    # Fetching the filtered data:
    dff = filters.process_filter(df_monthly, value_vessel, value_segment, value_owner, value_operator,
                                 value_tanks, value_dock_scrub)

    # Deleting duplicate entries:
    dff = dff.drop_duplicates(subset='Vessel name')

    if n_clicks:
        return {
            'data': [go.Bar(name='HFO Jan', x=dff['Vessel name'], y=dff['HFO Jan'], marker_color='#F8DFE1'),
                     go.Bar(name='HFO Feb', x=dff['Vessel name'], y=dff['HFO Feb'], marker_color='#F6D7D9'),
                     go.Bar(name='HFO Mar', x=dff['Vessel name'], y=dff['HFO Mar'], marker_color='#F4CDCF'),
                     go.Bar(name='HFO Apr', x=dff['Vessel name'], y=dff['HFO Apr'], marker_color='#F1C0C3'),
                     go.Bar(name='HFO May', x=dff['Vessel name'], y=dff['HFO May'], marker_color='#EEB0B4'),
                     go.Bar(name='HFO Jun', x=dff['Vessel name'], y=dff['HFO Jun'], marker_color='#EA9CA1'),
                     go.Bar(name='HFO Jul', x=dff['Vessel name'], y=dff['HFO Jul'], marker_color='#E58389'),
                     go.Bar(name='HFO Aug', x=dff['Vessel name'], y=dff['HFO Aug'], marker_color='#DF646B'),
                     go.Bar(name='HFO Sep', x=dff['Vessel name'], y=dff['HFO Sep'], marker_color='#D73D46'),
                     go.Bar(name='HFO Oct', x=dff['Vessel name'], y=dff['HFO Oct'], marker_color='#CD0C18'),
                     go.Bar(name='HFO Nov', x=dff['Vessel name'], y=dff['HFO Nov'], marker_color='#A40A13'),
                     go.Bar(name='HFO Dec', x=dff['Vessel name'], y=dff['HFO Dec'], marker_color='#83080F'),
                     ],
            'layout': go.Layout(
                barmode='stack',
                xaxis={'title': 'Vessel Name', 'autorange': True},
                yaxis={'title': 'Consumption[Tons]'},
                margin={'l': 80, 'b': 150, 't': 10, 'r': 80},
                autosize=True,
                legend=dict(x=0, y=1, orientation='h')
            )
        }

    # Returning the filtered data to the graph
    return {
        'data': [go.Bar(name='HFO Jan', x=dff['Vessel name'], y=dff['HFO Jan'], marker_color='#F8DFE1'),
                 go.Bar(name='HFO Feb', x=dff['Vessel name'], y=dff['HFO Feb'], marker_color='#F6D7D9'),
                 go.Bar(name='HFO Mar', x=dff['Vessel name'], y=dff['HFO Mar'], marker_color='#F4CDCF'),
                 go.Bar(name='HFO Apr', x=dff['Vessel name'], y=dff['HFO Apr'], marker_color='#F1C0C3'),
                 go.Bar(name='HFO May', x=dff['Vessel name'], y=dff['HFO May'], marker_color='#EEB0B4'),
                 go.Bar(name='HFO Jun', x=dff['Vessel name'], y=dff['HFO Jun'], marker_color='#EA9CA1'),
                 go.Bar(name='HFO Jul', x=dff['Vessel name'], y=dff['HFO Jul'], marker_color='#E58389'),
                 go.Bar(name='HFO Aug', x=dff['Vessel name'], y=dff['HFO Aug'], marker_color='#DF646B'),
                 go.Bar(name='HFO Sep', x=dff['Vessel name'], y=dff['HFO Sep'], marker_color='#D73D46'),
                 go.Bar(name='HFO Oct', x=dff['Vessel name'], y=dff['HFO Oct'], marker_color='#CD0C18'),
                 go.Bar(name='HFO Nov', x=dff['Vessel name'], y=dff['HFO Nov'], marker_color='#A40A13'),
                 go.Bar(name='HFO Dec', x=dff['Vessel name'], y=dff['HFO Dec'], marker_color='#83080F'),
                 ],
        'layout': go.Layout(
            barmode='stack',
            xaxis={'title': 'Vessel Name', 'autorange': True},
            yaxis={'title': 'Consumption[Tons]'},
            margin={'l': 80, 'b': 150, 't': 10, 'r': 80},
            autosize=True,
            legend=dict(x=0, y=1, orientation='h')
        )
    }


# Callback for stock table on the monthly consumption page7
@app.callback(
    Output('datatable-stock', 'data'),
    [Input('datatable-stock', "page_current"),
     Input('datatable-stock', "page_size"),
     Input('dd_vessel', "value"),
     Input('dd_segment', "value"),
     Input('dd_owner', "value"),
     Input('dd_operator', 'value'),
     Input('dd_tanks', 'value'),
     Input('dd_dock_scrub', 'value'),
     Input('datatable-stock', 'sort_by')])
def update_stock_monthly(page_current, page_size, value_vessel, value_segment, value_owner, value_operator,
                         value_tanks, value_dock_scrub, sort_by):
    # Fetching the filtered data:
    dff_temp = filters.process_filter(df_monthly, value_vessel, value_segment, value_owner, value_operator,
                                      value_tanks, value_dock_scrub)

    # Deleting duplicate entries:
    dff_temp = dff_temp.drop_duplicates(subset='Vessel name')

    dff_temp = dff_temp.sort_values(by='Burn Oct', ascending=False)

    if len(sort_by):
        dff = dff_temp.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = dff_temp

    # Returning the filtered data to the table
    return dff.iloc[
           :(page_current + 1) * page_size
           ].to_dict('records')


# To enable marker lines use the below code in the graph plots:
# marker_line_color = 'rgb(70,130,180)', marker_line_width = 1.0

# Run the Dash app
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
