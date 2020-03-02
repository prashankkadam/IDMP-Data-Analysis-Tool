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

app.config.suppress_callback_exceptions = True

df = pd.read_csv('data/bcw.csv')

df[' index'] = range(1, len(df) + 1)

colnames = df.columns

PAGE_SIZE = 15

tab1_content = dbc.Card(
    dbc.CardBody([
        # html.Div([
        # dcc.Upload(
        #     id='upload-data',
        #     children=html.Div([
        #         'Drag and Drop or ',
        #         html.A('Select Files')
        #     ]),
        #         style={
        #             'width': '100%',
        #             'height': '60px',
        #             'lineHeight': '60px',
        #             'borderWidth': '1px',
        #             'borderStyle': 'dashed',
        #             'borderRadius': '5px',
        #             'textAlign': 'center',
        #             'margin': '10px'
        #         },
        #         # Allow multiple files to be uploaded
        #         multiple=True
        #     )
        # ]),
        'Select Columns: ',
        dcc.Dropdown(
            id='dropdown-select-column',
            options=[{
                'label': i,
                'value': i
            } for i in colnames.dropna().unique()],
            multi=True
        ),
        html.Br(),
        dash_table.DataTable(
            id='datatable',
            columns=[
                {"name": i, "id": i} for i in sorted(df.columns)
            ],
            page_current=0,
            page_size=PAGE_SIZE,
            page_action='custom',
            style_table={'overflowX': 'scroll'},

            sort_action='custom',
            sort_mode='single',
            sort_by=[]
        ),
        html.Br(),
        'Row count: ',
        dcc.Input(
            id='datatable-row-count',
            type='number',
            min=1,
            max=100,
            value=15
        )
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
        dbc.Tab(tab1_content, id='tab_table', label="Data Table",
                label_style={'font-weight': 'bold', 'font-size': '20px', 'color': 'grey'}),
        dbc.Tab(tab2_content, id='tab_plot', label="Plot",
                label_style={'font-weight': 'bold', 'font-size': '20px', 'color': 'grey'}),
        dbc.Tab(tab3_content, id='tab_quant', label="Quantization",
                label_style={'font-weight': 'bold', 'font-size': '20px', 'color': 'grey'})
    ])
])

app.layout = layout


@app.callback(
    Output('datatable', 'data'),
    [Input('datatable', "page_current"),
     Input('datatable', "page_size"),
     Input('datatable', 'sort_by'),
     Input('datatable-row-count', 'value'),
     Input('dropdown-select-column', 'value')])
def update_table(page_current, page_size, sort_by, row_count_value, selected_cols):
    if row_count_value is not None:
        page_size = row_count_value

    if len(sort_by):
        dff = df.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = df

    if selected_cols is not None:
        if len(selected_cols) != 0:
            return dff[selected_cols].iloc[
                   page_current * page_size:(page_current + 1) * page_size
                   ].to_dict('records')
        else:
            return dff.iloc[
                   page_current * page_size:(page_current + 1) * page_size
                   ].to_dict('records')
    else:
        return dff.iloc[
               page_current * page_size:(page_current + 1) * page_size
               ].to_dict('records')


if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
