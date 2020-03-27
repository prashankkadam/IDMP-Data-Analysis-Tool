from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import base64
import io
import os
import pandas as pd
import dash

print(dcc.__version__)  # 0.6.0 or above is required

app = dash.Dash()
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    # This is the 'hidden div' however its really a container for sub-divs, some hidden, some not
    html.Div(id='output-data-upload'),
    html.Br(),
    html.Div(id='page-content')
])

index_page = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '30%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
    ),

    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
])

page_1_layout = html.Div([
    # This button will pull the JSON data into a new callback
    html.Button('Submit', id='button'),
    html.Div(id='output-container-button'),
    html.Div(id='page-1-content'),
    dcc.Link('Go to Page 2', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),

])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return filename, df


page_2_layout = html.Div([
    html.Div(id='page-2-content'),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])


# Update the index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename'),
               Input('upload-data', 'last_modified')])
def update_output(contents, filename, date):
    if contents is not None:
        filename, df = parse_contents(contents, filename, date)
        # This is the key to the hidden div formatting
        return html.Div([
            html.Div(['Tank Stats file: ' + filename]),
            html.Div([df.to_json(orient='split')], id='tankStats', style={'display': 'none'})
        ], style={'padding-top': '60px', 'align': "center"})


@app.callback(Output('output-container-button', 'children'),
              [Input('button', 'n_clicks'),
               Input('tankStats', 'children')])
def update_graph(n_clicks, tankStats):
    if n_clicks is not None:
        dff = pd.read_json(tankStats[0], orient='split')
        print(dff)
        # figure = create_figure(dff)
        return 'pass success'


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "https://fonts.googleapis.com/css?family=Work+Sans",
                "https://bootswatch.com/3/paper/bootstrap.css"]
# 'https://codepen.io/chriddyp/pen/bWLwgP.css']

for css in external_css:
    app.css.append_css({"external_url": css})

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })

if __name__ == '__main__':
    app.run_server(debug=True)
