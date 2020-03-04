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

#############################################################################################
# Tab 2 previous layout code
# tab2_content = dbc.Card(
#     dbc.CardBody([
#         dbc.Row([
#             dbc.Col([], width="auto", style={"padding": "1%"}),
#             dbc.Col([
#                 html.Div('Graph:', style={'color': 'grey', 'fontSize': 18})
#             ], width="auto", style={"padding": "5px"}),
#             dbc.Col([
#                 dcc.Dropdown(
#                     id='graph-select-dropdown',
#                     options=[
#                         {'label': 'Scatter', 'value': 'Sctplt'},
#                         {'label': 'Bar', 'value': 'Barplt'},
#                         {'label': 'Box', 'value': 'Linplt'}
#                     ],
#                     value='Sctplt'
#                 )
#             ], width=1, style={"padding": "5px"}),
#             dbc.Col([], width="auto", style={"padding": "2%"}),
#             dbc.Col([
#                 html.Div('X label:', style={'color': 'grey', 'fontSize': 18})
#             ], width="auto", style={"padding": "5px"}),
#             dbc.Col([
#                 dcc.Dropdown(
#                     id='xlab-select-dropdown',
#                     options=[{
#                         'label': i,
#                         'value': i
#                     } for i in list(set(numeric_cols))]
#                 )
#             ], width=1, style={"padding": "5px"}),
#             dbc.Col([], width="auto", style={"padding": "2%"}),
#             dbc.Col([
#                 html.Div('Y label:', style={'color': 'grey', 'fontSize': 18})
#             ], width="auto", style={"padding": "5px"}),
#             dbc.Col([
#                 dcc.Dropdown(
#                     id='ylab-select-dropdown',
#                     options=[{
#                         'label': i,
#                         'value': i
#                     } for i in list(set(numeric_cols))]
#                 )
#             ], width=1, style={"padding": "5px"}),
#             dbc.Col([], width="auto", style={"padding": "2%"}),
#             dbc.Col([
#                 html.Div('Color:', style={'color': 'grey', 'fontSize': 18})
#             ], width="auto", style={"padding": "5px"}),
#             dbc.Col([
#                 dcc.Dropdown(
#                     id='col-select-dropdown',
#                     options=[{
#                         'label': i,
#                         'value': i
#                     } for i in list(set(numeric_cols))]
#                 )
#             ], width=1, style={"padding": "5px"}),
#             dbc.Col([], width="auto", style={"padding": "2%"}),
#             dbc.Col([
#                 html.Div('Size:', style={'color': 'grey', 'fontSize': 18})
#             ], width="auto", style={"padding": "5px"}),
#             dbc.Col([
#                 dcc.Dropdown(
#                     id='siz-select-dropdown',
#                     options=[{
#                         'label': i,
#                         'value': i
#                     } for i in list(set(numeric_cols))]
#                 )
#             ], width=1, style={"padding": "5px"}),
#             dbc.Col([], width="auto", style={"padding": "2%"}),
#             dbc.Col([
#                 html.Div('Facet:', style={'color': 'grey', 'fontSize': 18})
#             ], width="auto", style={"padding": "5px"}),
#             dbc.Col([
#                 dcc.Dropdown(
#                     id='fac-select-dropdown',
#                     options=[{
#                         'label': i,
#                         'value': i
#                     } for i in list(set(numeric_cols))]
#                 )
#             ], width=1, style={"padding": "5px"})
#         ], no_gutters=True),
#         dbc.Row([
#             dcc.Graph(id="plot-graph", style={"width": "75%"})
#         ]),
#     ]),
#     className="mt-3",
# )
##################################################################################################

# import plotly.express as px
# import pandas as pd
# from plotly.offline import plot
#
# df = pd.read_csv('data/bcw.csv')
# fig = px.box(df, x="diagnosis", y="texture_mean", color="")
# plot(fig)
#
# from scipy.stats import shapiro
# import pandas as pd
#
# df = pd.read_csv('data/bcw.csv')
# data = [0.873, 2.817, 0.121, -0.945, -0.055, -1.436, 0.360, -1.478, -1.637, -1.869]
# stat, p = shapiro(list(df["radius_mean"]))
# print('stat=%.3f, p=%.3f' % (stat, p))
# if p > 0.05:
# 	print('Probably Gaussian')
# else:
# 	print('Probably not Gaussian')
#



# def create_callback(output):
#     def callback(input_value):
#         input_value = input_value.lower()
#         if input_value in output:
#             return {'display': 'block'}
#         return {'display': 'none'}
#
#     return callback
#
#
# for output_element in output_elements:
#     dynamically_generated_function = create_callback(output_element)
#     app.callback(Output(output_element, 'style'),
#                  [Input('hypothesis-dropdown', 'values')])(dynamically_generated_function)


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash('example')

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown-to-show_or_hide-element',
        options=[
            {'label': 'Show element', 'value': 'on'},
            {'label': 'Hide element', 'value': 'off'}
        ],
        value='on'
    ),

    # Create Div to place a conditionally visible element inside
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Input(
            id='element-to-hide',
            placeholder='something',
            value='Can you see me?',
        )
    ], style={'display': 'block'}  # <-- This is the line that will be changed by the dropdown callback
    )
])


@app.callback(
    Output(component_id='element-to-hide', component_property='style'),
    [Input(component_id='dropdown-to-show_or_hide-element', component_property='value')])
def show_hide_element(visibility_state):
    if visibility_state == 'on':
        return {'display': 'block'}
    if visibility_state == 'off':
        return {'display': 'none'}


if __name__ == '__main__':
    app.run_server(debug=True)
