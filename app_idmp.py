import base64
import datetime
import io

import dash
import os
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
from flask import Flask, render_template
from flask_basicauth import BasicAuth
from layouts import navs
from apps import idmp_tool as idmp
import pandas as pd

# Creating a flask server
server = Flask(__name__)

# Hardcoding the basic auth user name and password
server.config['BASIC_AUTH_USERNAME'] = 'admin'
server.config['BASIC_AUTH_PASSWORD'] = 'idmpspr2020'

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

# df_data = pd.read_csv('data/bcw.csv')
#
# df_data[' index'] = range(1, len(df_data) + 1)

PAGE_SIZE = 15


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            df[' index'] = range(1, len(df) + 1)
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            df[' index'] = range(1, len(df) + 1)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        # html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            id='datatable-paging',
            data=df.to_dict('records'),
            columns=[
                {"name": i, "id": i} for i in sorted(df.columns)
            ],
            page_current=0,
            page_size=PAGE_SIZE,
            page_action='custom',
            style_table={'overflowX': 'scroll'}
        ),

        # html.Hr(),  # horizontal line
        #
        # # For debugging, display the raw contents provided by the web browser
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })
    ])


tab1_content = dbc.Card(
    dbc.CardBody([
        html.Div([
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            html.Div(id='output-data-upload'),
        ]),
        html.Div([
            dash_table.DataTable(
                id='datatable-paging'
            )
        ])
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

layout = html.Div([dbc.Tabs(
    [
        dbc.Tab(tab1_content, id='tab_rob_1', label="Data Table",
                label_style={'font-weight': 'bold', 'font-size': '20px', 'color': 'grey'}),
        dbc.Tab(tab2_content, id='tab_rob_2', label="Plot",
                label_style={'font-weight': 'bold', 'font-size': '20px', 'color': 'grey'}),
        dbc.Tab(tab3_content, id='tab_rob_3', label="Quantization",
                label_style={'font-weight': 'bold', 'font-size': '20px', 'color': 'grey'})
    ])
])

app.layout = layout


# @app.callback(
#     Output('datatable-paging', 'data'),
#     [Input('datatable-paging', "page_current"),
#      Input('datatable-paging', "page_size")])
# def update_table(page_current, page_size):
#     return df.iloc[
#            page_current * page_size:(page_current + 1) * page_size
#            ].to_dict('records')


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        return children


if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
