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
import plotly.express as px
import plotly.graph_objs as go

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
dtype_mapping = dict(df.dtypes)
numeric_cols = [c for c in colnames if dtype_mapping[c] != 'O']
catagory_cols = [c for c in colnames if dtype_mapping[c] == 'O']

PAGE_SIZE = 15
dimensions = ["x", "y", "color", "facet_col", "facet_row"]
graph_types = ["Scatter", "Bar", "Box", "Heatmap"]

col_options = [dict(label=x, value=x) for x in df.columns]
num_options = [dict(label=x, value=x) for x in list(set(numeric_cols))]
cat_options = [dict(label=x, value=x) for x in list(set(catagory_cols))]
graph_options = [dict(label=x, value=x) for x in graph_types]

tab1_content = dbc.Card(
    dbc.CardBody([
        # html.Div([
        # dcc.Upload(
        #     id='upload-data',
        #     children=html.Div([
        #         'Drag and Drop or ',
        #         html.A('Select Files')
        #     ]),
        #     style={
        #         'width': '100%',
        #         'height': '60px',
        #         'lineHeight': '60px',
        #         'borderWidth': '1px',
        #         'borderStyle': 'dashed',
        #         'borderRadius': '5px',
        #         'textAlign': 'center',
        #         'margin': '10px'
        #     },
        #     # Allow multiple files to be uploaded
        #     multiple=True
        # )
        # ]),
        dbc.Row([
            dbc.Col([
                html.Div('Filter Columns', style={'color': 'grey', 'fontSize': 18}),
            ]),
            dbc.Col([
                dcc.Dropdown(
                    id='dropdown-select-column',
                    options=[{
                        'label': i,
                        'value': i
                    } for i in colnames.dropna().unique()],
                    multi=True
                ),
            ], width=11)
        ]),
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
            sort_by=[],

            filter_action='custom',
            filter_query=''
        ),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Div('Row Count ', style={'color': 'grey', 'fontSize': 14}),
            ]),
            dbc.Col([
                dcc.Input(
                    id='datatable-row-count',
                    type='number',
                    min=1,
                    max=100,
                    value=15
                )
            ], width=11),
        ]),
    ]),
    className="mt-3",
)

tab2_content = html.Div(
    [
        html.Div(
            [
                html.P(["Graph" + ":", dcc.Dropdown(id="graph-select-dropdown", options=graph_options,
                                                    value="Scatter")]),
                html.P(["X label" + ":", dcc.Dropdown(id="xlab-select-dropdown", options=col_options)]),
                html.P(["Y label" + ":", dcc.Dropdown(id="ylab-select-dropdown", options=col_options)]),
                html.P(["Color" + ":", dcc.Dropdown(id="col-select-dropdown", options=col_options)]),
                html.P(["Size" + ":", dcc.Dropdown(id="siz-select-dropdown", options=col_options)]),
                html.P(["Facet" + ":", dcc.Dropdown(id="fac-select-dropdown", options=col_options)]),
            ],
            style={"width": "25%", "float": "left", "padding": "20px"},
        ),
        dcc.Graph(id="plot-graph", style={"width": "75%", "display": "inline-block"}),
    ]
)

hypothesis_tests = ["Normality", "Correlation", "Parametric"]
normality_tests = ["Shapiro-Wilk", "D’Agostino’s K^2", "Anderson-Darling"]
correlation_tests = ["Pearson", "Spearman", "Kendall", "Chi-Squared"]
parametric_tests = ["Student t-test", "Paired Student t-test", "ANOVA", "Repeated ANOVA"]

hypothesis_options = [dict(label=x, value=x) for x in hypothesis_tests]
normality_options = [dict(label=x, value=x) for x in normality_tests]
correlation_options = [dict(label=x, value=x) for x in correlation_tests]
parametric_options = [dict(label=x, value=x) for x in parametric_tests]

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

norm_tab = dbc.Card(
    dbc.CardBody([
        html.Div(
            [
                html.P(
                    ["Normality Tests" + ":", dcc.Dropdown(id="normality-dropdown",
                                                           options=normality_options)]),
                html.P(
                    ["Test Variable" + ":", dcc.Dropdown(id="test-var1-dropdown",
                                                         options=num_options)]),
            ],
            style={"width": "25%", "float": "left", "padding": "20px"},
        ),
        html.Div(id="norm-tab"),
    ]),
    className="mt-3",
)

corr_tab = dbc.Card(
    dbc.CardBody([
        html.Div(
            [
                html.P(
                    ["Correlation Tests" + ":", dcc.Dropdown(id="correlation-dropdown",
                                                             options=correlation_options)]),
                html.P(
                    ["Test Variable" + ":", dcc.Dropdown(id="test-var2-dropdown",
                                                         options=num_options)]),
            ],
            style={"width": "25%", "float": "left", "padding": "20px"},
        ),
        html.Div(id="corr-tab"),
    ]),
    className="mt-3",
)

para_tab = dbc.Card(
    dbc.CardBody([
        html.Div(
            [
                html.P(
                    ["Parametric Tests" + ":", dcc.Dropdown(id="parametric-dropdown",
                                                            options=parametric_options)]),
                html.P(
                    ["Test Variable" + ":", dcc.Dropdown(id="test-var3-dropdown",
                                                         options=num_options)]),
            ],
            style={"width": "25%", "float": "left", "padding": "20px"},
        ),
        html.Div(id="para-tab"),
    ]),
    className="mt-3",
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
                dcc.Tab(children=norm_tab,
                        label='Normality',
                        value='tab-1',
                        style=tab_style,
                        selected_style=tab_selected_style),
                dcc.Tab(children=corr_tab,
                        label='Correlation',
                        value='tab-2',
                        style=tab_style,
                        selected_style=tab_selected_style),
                dcc.Tab(children=para_tab,
                        label='Parametric',
                        value='tab-3',
                        style=tab_style,
                        selected_style=tab_selected_style),
                # dcc.Tab(label='Tab 4', value='tab-4', style=tab_style, selected_style=tab_selected_style),
            ], style=tabs_styles)
        ]

    ),
    className="mt-3",
)

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if v0 == value_part[-1] and v0 in ("'", '"', '`'):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


layout = html.Div([dbc.Tabs(
    [
        dbc.Tab(tab1_content, id='tab_table', label="Data Table",
                label_style={'font-weight': 'bold', 'font-size': '20px', 'color': 'grey'}),
        dbc.Tab(tab2_content, id='tab_plot', label="Plot",
                label_style={'font-weight': 'bold', 'font-size': '20px', 'color': 'grey'}),
        dbc.Tab(tab3_content, id='tab_quant', label="Quantization",
                label_style={'font-weight': 'bold', 'font-size': '20px', 'color': 'grey'}),
        html.Div(id='df_json', style={'display': 'none'})
    ])
])

app.layout = layout


@app.callback(
    Output('datatable', 'data'),
    [Input('datatable', "page_current"),
     Input('datatable', "page_size"),
     Input('datatable', 'sort_by'),
     Input('datatable', "filter_query"),
     Input('datatable-row-count', 'value'),
     Input('dropdown-select-column', 'value')])
def update_table(page_current, page_size, sort_by, filter, row_count_value, selected_cols):
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

    if filter is not None:
        filtering_expressions = filter.split(' && ')

        for filter_part in filtering_expressions:
            col_name, operator, filter_value = split_filter_part(filter_part)

            if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                # these operators match pandas series operator method names
                dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
            elif operator == 'contains':
                dff = dff.loc[dff[col_name].str.contains(filter_value)]
            elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                dff = dff.loc[dff[col_name].str.startswith(filter_value)]

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


@app.callback(Output("plot-graph", "figure"),
              [Input("graph-select-dropdown", "value"),
               Input("xlab-select-dropdown", "value"),
               Input("ylab-select-dropdown", "value"),
               Input("col-select-dropdown", "value"),
               Input("siz-select-dropdown", "value"),
               Input("fac-select-dropdown", "value")])
def make_figure(graph, xlab, ylab, color, size, facet):
    if graph == "Scatter" or graph is None:
        return px.scatter(
            df,
            x=xlab,
            y=ylab,
            color=color,
            size=size,
            facet_col=facet,
            height=700,
        )
    elif graph == "Bar":
        return px.bar(
            df,
            x=xlab,
            y=ylab,
            color=color,
            facet_col=facet,
            height=700,
        )
    elif graph == "Box":
        return px.box(
            df,
            x=xlab,
            y=ylab,
            color=color,
            facet_col=facet,
            height=700,
        )
    elif graph == "Heatmap":
        return px.density_heatmap(
            df,
            x=xlab,
            y=ylab,
            facet_col=facet,
            height=700,
        )


if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
