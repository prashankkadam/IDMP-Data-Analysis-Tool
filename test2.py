import base64
import datetime
import io

import dash
# from dash.dependencies import Input, Output, State
# import dash_core_components as dcc
# import dash_html_components as html
# import dash_table
#
# import pandas as pd
#
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#
# app.config.suppress_callback_exceptions = True
#
# PAGE_SIZE = 15
#
# app.layout = html.Div([
#     html.Div([
#         dcc.Upload(
#             id='upload-data',
#             children=html.Div([
#                 'Drag and Drop or ',
#                 html.A('Select Files')
#             ]),
#             style={
#                 'width': '100%',
#                 'height': '60px',
#                 'lineHeight': '60px',
#                 'borderWidth': '1px',
#                 'borderStyle': 'dashed',
#                 'borderRadius': '5px',
#                 'textAlign': 'center',
#                 'margin': '10px'
#             },
#             # Allow multiple files to be uploaded
#             multiple=False
#         )
#     ]),
#     # html.Div(id='output-data-upload'),
#     html.Div([
#         dash_table.DataTable(
#             id='datatable-paging',
#             page_current=0,
#             page_size=PAGE_SIZE,
#             page_action='custom'
#         )
#     ]),
#     html.Div([
#         dcc.Graph(
#             id='test-scatter',
#         )
#     ]),
#
#     # Hidden div inside the app that stores the intermediate value
#     html.Div(id='intermediate-value', style={'display': 'none'})
# ])
#
#
# @app.callback(Output('intermediate-value', 'children'),
#               [Input('upload-data', 'contents')],
#               [State('upload-data', 'filename')])
# def read_data(content, filename):
#     if content is not None:
#         content_type, content_string = content.split(',')
#         decoded = base64.b64decode(content_string)
#
#         if 'csv' in filename:
#             # Assume that the user uploaded a CSV file
#             df = pd.read_csv(
#                 io.StringIO(decoded.decode('utf-8')))
#             print(df)
#             return df.to_json(date_format='iso', orient='split')
#         elif 'xls' in filename:
#             # Assume that the user uploaded an excel file
#             df = pd.read_excel(io.BytesIO(decoded))
#             return df.to_json(date_format='iso', orient='split')
#
#
# @app.callback(Output('datatable-paging', 'rows'),
#               [Input('datatable-paging', "page_current"),
#                Input('datatable-paging', "page_size"),
#                Input('intermediate-value', 'children')])
# def update_table(page_current, page_size, jsonified_cleaned_data):
#     if jsonified_cleaned_data is not None:
#         df = pd.read_json(jsonified_cleaned_data, orient='split')
#         print(df)
#         print(page_current)
#         print(page_size)
#
#         return df.iloc[
#                page_current * page_size:(page_current + 1) * page_size
#                ].to_dict('records')


# @app.callback(
#     dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
#     [Input('intermediate-value', 'children')])
# def update_graph(jsonified_cleaned_data):
#     if jsonified_cleaned_data is not None:
#         df = pd.read_json(jsonified_cleaned_data, orient='split')
#         print("scatter" + df)
#         return {
#             'data': [dict(
#                 x=df['fractal_dimension_worst'],
#                 y=df['radius_mean'],
#                 mode='markers',
#                 marker={
#                     'size': 15,
#                     'opacity': 0.5,
#                     'line': {'width': 0.5, 'color': 'white'}
#                 }
#             )],
#         }


# if __name__ == '__main__':
#     app.run_server(debug=True)


import plotly.express as px
import pandas as pd
from plotly.offline import plot

df = pd.read_csv('data/bcw.csv')
fig = px.box(df, x="diagnosis", y="texture_mean", color="")
plot(fig)
