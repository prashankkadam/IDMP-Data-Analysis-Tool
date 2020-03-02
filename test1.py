import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

################################################################################################################

global_df = pd.read_csv('...')
app.layout = html.Div([
    dcc.Graph(id='graph'),
    html.Table(id='table'),
    dcc.Dropdown(id='dropdown'),

    # Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate-value', style={'display': 'none'})
])


@app.callback(Output('intermediate-value', 'children'), [Input('dropdown', 'value')])
def clean_data(value):
    # some expensive clean data step
    cleaned_df = your_expensive_clean_or_compute_step(value)

    # more generally, this line would be
    # json.dumps(cleaned_df)
    return cleaned_df.to_json(date_format='iso', orient='split')


@app.callback(Output('graph', 'figure'), [Input('intermediate-value', 'children')])
def update_graph(jsonified_cleaned_data):
    # more generally, this line would be
    # json.loads(jsonified_cleaned_data)
    dff = pd.read_json(jsonified_cleaned_data, orient='split')

    figure = create_figure(dff)
    return figure


@app.callback(Output('table', 'children'), [Input('intermediate-value', 'children')])
def update_table(jsonified_cleaned_data):
    dff = pd.read_json(jsonified_cleaned_data, orient='split')
    table = create_table(dff)
    return table


###############################################################################################################


# PAGE_SIZE = 15
#
# app.layout = html.Div([
#     dcc.Upload(
#         id='upload-data',
#         children=html.Div([
#             'Drag and Drop or ',
#             html.A('Select Files')
#         ]),
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
#     ),
#     html.Div(id='output-data-upload'),
#     # dash_table.DataTable(id='table')
# ])


# def parse_contents(contents, filename, date):
#     content_type, content_string = contents.split(',')
#
#     decoded = base64.b64decode(content_string)
#     try:
#         if 'csv' in filename:
#             # Assume that the user uploaded a CSV file
#             df = pd.read_csv(
#                 io.StringIO(decoded.decode('utf-8')))
#             df[' index'] = range(1, len(df) + 1)
#         elif 'xls' in filename:
#             # Assume that the user uploaded an excel file
#             df = pd.read_excel(io.BytesIO(decoded))
#             df[' index'] = range(1, len(df) + 1)
#     except Exception as e:
#         print(e)
#         return html.Div([
#             'There was an error processing this file.'
#         ])
#
#     return html.Div([
#         html.H5(filename),
#         html.H6(datetime.datetime.fromtimestamp(date)),
#
#         dash_table.DataTable(
#             id='table',
#             data=df.iloc[
#                  0 * PAGE_SIZE:(0 + 1) * PAGE_SIZE
#                  ].to_dict('records'),
#             columns=[{'name': i, 'id': i} for i in df.columns],
#             page_action='custom'
#         ),
#
#         html.Hr(),  # horizontal line
#
#         # For debugging, display the raw contents provided by the web browser
#         html.Div('Raw Content'),
#         html.Pre(contents[0:200] + '...', style={
#             'whiteSpace': 'pre-wrap',
#             'wordBreak': 'break-all'
#         })
#     ])


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, page_current, list_of_names, list_of_dates):
    if list_of_contents is not None:
        for contents, filename, date in zip(list_of_contents, list_of_names, list_of_dates):
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

            children = [
                html.Div([
                    html.H5(filename),
                    html.H6(datetime.datetime.fromtimestamp(date)),

                    dash_table.DataTable(
                        id='table',
                        data=df.iloc[
                             page_current * PAGE_SIZE:(page_current + 1) * PAGE_SIZE
                             ].to_dict('records'),
                        columns=[{'name': i, 'id': i} for i in df.columns],
                        page_action='custom'
                    ),

                    html.Hr(),  # horizontal line

                    # For debugging, display the raw contents provided by the web browser
                    html.Div('Raw Content'),
                    html.Pre(contents[0:200] + '...', style={
                        'whiteSpace': 'pre-wrap',
                        'wordBreak': 'break-all'
                    })
                ])
            ]
#         # children = [
#         #     parse_contents(c, n, d) for c, n, d in
#         #     zip(list_of_contents, list_of_names, list_of_dates)]
#         return children


# @app.callback(
#     [Output('table', 'data'),
#      Output('output-data-upload', 'data')],
#     [Input('table-page-count', "page_current"),
#      Input('table-page-count', "page_size"),
#      Input('upload-data', 'contents')],
#     [State('upload-data', 'filename')])
# def update_table(page_current, page_size, contents, filename):
#     content_type, content_string = contents.split(',')
#
#     decoded = base64.b64decode(content_string)
#     try:
#         if 'csv' in filename:
#             # Assume that the user uploaded a CSV file
#             df = pd.read_csv(
#                 io.StringIO(decoded.decode('utf-8')))
#             df[' index'] = range(1, len(df) + 1)
#             children = zip(df.iloc[
#                            page_current * page_size:(page_current + 1) * page_size
#                            ].to_dict('records'))
#         elif 'xls' in filename:
#             # Assume that the user uploaded an excel file
#             df = pd.read_excel(io.BytesIO(decoded))
#             df[' index'] = range(1, len(df) + 1)
#             children = zip(df.iloc[
#                            page_current * page_size:(page_current + 1) * page_size
#                            ].to_dict('records'))
#     except Exception as e:
#         print(e)
#         return html.Div([
#             'There was an error processing this file.'
#         ])
#     return children


# df.iloc[
#            page_current * page_size:(page_current + 1) * page_size
#            ].to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
