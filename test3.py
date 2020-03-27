import base64
import io

import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
from scipy.stats import shapiro, normaltest, anderson, \
    pearsonr, spearmanr, kendalltau, chi2_contingency, \
    ttest_ind, ttest_rel, f_oneway

# Statmodels installation required for trendline
data_name = ""
df_up = pd.DataFrame()
df = pd.read_csv('data/bcw.csv')

df.insert(loc=0, column=' index', value=range(1, len(df) + 1))

colnames = df.columns
dtype_mapping = dict(df.dtypes)
numeric_cols = [c for c in colnames if dtype_mapping[c] != 'O']
catagory_cols = [c for c in colnames if dtype_mapping[c] == 'O']

PAGE_SIZE = 10
# dsp_yes = {'display': 'initial'}
# dsp_no = {'display': 'none'}
dimensions = ["x", "y", "color", "facet_col", "facet_row"]
graph_types = ["Scatter", "Bar", "Box", "Heatmap"]
hypothesis_tests = ["Normality", "Correlation", "Parametric"]
normality_tests = ["Shapiro-Wilk", "D’Agostino’s K^2", "Anderson-Darling"]
correlation_tests = ["Pearson", "Spearman", "Kendall", "Chi-Squared"]
parametric_tests = ["Student t-test", "Paired Student t-test", "ANOVA"]

col_options = [dict(label=x, value=x) for x in df.columns]
num_options = [dict(label=x, value=x) for x in list(set(numeric_cols))]
cat_options = [dict(label=x, value=x) for x in list(set(catagory_cols))]
graph_options = [dict(label=x, value=x) for x in graph_types]

hypothesis_options = [dict(label=x, value=x) for x in hypothesis_tests]
normality_options = [dict(label=x, value=x) for x in normality_tests]
correlation_options = [dict(label=x, value=x) for x in correlation_tests]
parametric_options = [dict(label=x, value=x) for x in parametric_tests]

upd_scat_x = 0

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
    'backgroundColor': '#17a2b8',
    'color': 'white',
    'padding': '6px'
}

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(
    __name__, external_stylesheets=external_stylesheets
)

app.config.suppress_callback_exceptions = True

IDMP_LOGO = 'idmp_logo.png'
ENCODED_URL = 'data:image/png;base64,{}'

# Encoding the IDMP logo
logo_enc = base64.b64encode(open(IDMP_LOGO, 'rb').read())

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=ENCODED_URL.format(logo_enc.decode()), height="50px")),
                    dbc.Col(dbc.NavbarBrand("IDMP - Data Analysis Tool", className="ml-2"),
                            style={'font-weight': 'bold', 'color': '#17a2b8'}),
                ],
                align="center",
                no_gutters=True,
            ),
            # href="/apps/dat",
        ),
        dbc.NavbarToggler(id="navbar-toggler")
    ],
)

nav = html.Div([
    dbc.Nav(
        [
            dbc.NavLink("Data Table",
                        id="id_dat",
                        href="/apps/dat",
                        style={'min-width': '200px', 'color': '#17a2b8'}),
            dbc.NavLink("Plot",
                        id="id_plt",
                        href="/apps/plt",
                        style={'min-width': '150px', 'color': '#17a2b8'}),
            dbc.NavLink("Quantization",
                        id="id_qnt",
                        href="/apps/qnt",
                        style={'min-width': '200px', 'color': '#17a2b8'}),
            # dbc.NavLink("Disabled", disabled=True, href="#", style={'min-width': '200px', 'color': 'skyblue'}),
        ],
        id='id_nav'
    )
], style={'padding-top': '10px', 'padding-left': '50px', 'font-weight': 'bold', 'line-height': '30px',
          'font-size': '20px'})

app.layout = html.Div([
    navbar,
    nav,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/dat':
        return tab_data_content
    elif pathname == '/apps/plt':
        return tab_plot_content
    elif pathname == '/apps/qnt':
        return tab_qnt_content
    else:
        return tab_data_content


########################################################################################################################
tab_data_content = dbc.Card(
    dbc.CardBody([
        html.Div([
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
            # ),
            html.Div([
                html.P([dbc.Input(id="input-url", placeholder="Enter data URL", type="text")])
            ], style={"width": "89%", "float": "left"}),
            dbc.Button("Load",
                       id="load-button",
                       color="info",
                       className="mr-2",
                       style={"width": "10%",
                              "display": "inline-block"}),
            html.H2(id='data-name', style={"width": "99%", "float": "left"}),
            html.Div(id='no-data', style={'display': 'none'})
        ]),
        dash_table.DataTable(
            id='datatable',
            columns=[
                # {"name": [i, "test"], "id": i} for i in df.columns
                {"name": [i, "None"], "id": i} for i in df.columns
            ],
            # df.columns,
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
        html.P(["Row Count" + ":", dcc.Input(id="datatable-row-count",
                                             type='number',
                                             value=10)],
               style={"display": "inline-block", 'fontSize': 12}),
    ]),
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


########################################################################################################################
scat_tab = dbc.Card(
    dbc.CardBody([
        html.Div(
            [
                html.Div([dbc.Button("Load",
                                     id="load-button-scat",
                                     color="info",
                                     className="mr-2",
                                     style={"width": "100%",
                                            "display": "inline-block"})], style={"padding": "20px"}),
                html.P(["X label" + ":", dcc.Dropdown(id="xlab-scat", options=col_options)]),
                html.P(["Y label" + ":", dcc.Dropdown(id="ylab-scat", options=col_options)]),
                html.P(["Color" + ":", dcc.Dropdown(id="col-scat", options=col_options)]),
                html.P(["Size" + ":", dcc.Dropdown(id="siz-scat", options=col_options)]),
                html.P(["Facet Row" + ":", dcc.Dropdown(id="fac-scat-row", options=col_options)]),
                html.P(["Facet Column" + ":", dcc.Dropdown(id="fac-scat-col", options=col_options)]),
                html.P(["Trendline" + ":", dcc.Dropdown(id="trnd-scat",
                                                        options=[{'label': 'OLS', 'value': 'ols'},
                                                                 {'label': 'Lowess', 'value': 'lowess'}])])

            ],
            style={"width": "25%", "float": "left"},
        ),
        dcc.Graph(id="plot-scatter", figure={}, style={"width": "75%", "display": "inline-block", "height": 700}),
    ]),
    className="mt-3"
)

bar_tab = dbc.Card(
    dbc.CardBody([
        html.Div(
            [
                html.Div([dbc.Button("Load",
                                     id="load-button-bar",
                                     color="info",
                                     className="mr-2",
                                     style={"width": "100%",
                                            "display": "inline-block"})], style={"padding": "20px"}),
                html.P(["X label" + ":", dcc.Dropdown(id="xlab-bar", options=col_options)]),
                html.P(["Y label" + ":", dcc.Dropdown(id="ylab-bar", options=col_options)]),
                html.P(["Color" + ":", dcc.Dropdown(id="col-bar", options=col_options)]),
                html.P(["Type" + ":", dcc.Dropdown(id="typ-bar", options=[{'label': 'None', 'value': 'none'},
                                                                          {'label': 'Stacked', 'value': 'stack'},
                                                                          {'label': 'Dodged', 'value': 'dodge'}])]),
                html.P(["Facet Row" + ":", dcc.Dropdown(id="fac-bar-row", options=col_options)]),
                html.P(["Facet Column" + ":", dcc.Dropdown(id="fac-bar-col", options=col_options)]),
            ],
            style={"width": "25%", "float": "left"},
        ),
        dcc.Graph(id="plot-bar", figure={}, style={"width": "75%", "display": "inline-block", "height": 700}),
    ]),
    className="mt-3",
)

box_tab = dbc.Card(
    dbc.CardBody([
        html.Div(
            [
                html.Div([dbc.Button("Load",
                                     id="load-button-box",
                                     color="info",
                                     className="mr-2",
                                     style={"width": "100%",
                                            "display": "inline-block"})], style={"padding": "20px"}),
                html.P(["X label" + ":", dcc.Dropdown(id="xlab-box", options=col_options)]),
                html.P(["Y label" + ":", dcc.Dropdown(id="ylab-box", options=col_options)]),
                html.P(["Color" + ":", dcc.Dropdown(id="col-box", options=col_options)]),
                html.P(["Facet Row" + ":", dcc.Dropdown(id="fac-box-row", options=col_options)]),
                html.P(["Facet Column" + ":", dcc.Dropdown(id="fac-box-col", options=col_options)]),
            ],
            style={"width": "25%", "float": "left"},
        ),
        dcc.Graph(id="plot-box", figure={}, style={"width": "75%", "display": "inline-block", "height": 700}),
    ]),
    className="mt-3",
)

heat_tab = dbc.Card(
    dbc.CardBody([
        html.Div(
            [
                html.Div([dbc.Button("Load",
                                     id="load-button-heat",
                                     color="info",
                                     className="mr-2",
                                     style={"width": "100%",
                                            "display": "inline-block"})], style={"padding": "20px"}),
                html.P(["X label" + ":", dcc.Dropdown(id="xlab-heat", options=col_options)]),
                html.P(["Y label" + ":", dcc.Dropdown(id="ylab-heat", options=col_options)]),
                html.P(["Facet Row" + ":", dcc.Dropdown(id="fac-heat-row", options=col_options)]),
                html.P(["Facet Column" + ":", dcc.Dropdown(id="fac-heat-col", options=col_options)]),
            ],
            style={"width": "25%", "float": "left"},
        ),
        dcc.Graph(id="plot-heat", figure={}, style={"width": "75%", "display": "inline-block", "height": 700}),
    ]),
    className="mt-3",
)

tab_plot_content = dbc.Card(
    dbc.CardBody(
        [
            dcc.Tabs(id="tabs-plot", value='tab-scat', children=[
                dcc.Tab(children=scat_tab,
                        label='Scatter',
                        value='tab-scat',
                        style=tab_style,
                        selected_style=tab_selected_style),
                dcc.Tab(children=bar_tab,
                        label='Bar',
                        value='tab-bar',
                        style=tab_style,
                        selected_style=tab_selected_style),
                dcc.Tab(children=box_tab,
                        label='Box',
                        value='tab-box',
                        style=tab_style,
                        selected_style=tab_selected_style),
                dcc.Tab(children=heat_tab,
                        label='Heat Map',
                        value='tab-heat',
                        style=tab_style,
                        selected_style=tab_selected_style)
            ], style=tabs_styles),
            html.Div(id='no-data-plt', children=colnames, style={'display': 'none'})
        ]

    ),
    className="mt-3",
)

########################################################################################################################

norm_tab = dbc.Card(
    dbc.CardBody([
        html.Div(
            [
                html.P(
                    ["Normality Tests" + ":", dcc.Dropdown(id="norm-test",
                                                           options=normality_options)]),
                html.P(
                    ["Test Variable" + ":", dcc.Dropdown(id="norm-var",
                                                         options=num_options)]),
            ],
            style={"width": "25%", "float": "left", "padding": "20px"},
        ),
        dcc.Graph(id="plot-norm", figure={}, style={"width": "75%", "display": "inline-block", "height": 500}),
        html.Table([
            html.Tr(html.Td(id='norm-val1')),
            html.Tr(html.Td(id='norm-val2')),
            html.Tr(html.Td(id='norm-val3')),
            html.Tr(html.Td(id='norm-val4')),
            html.Tr(html.Td(id='norm-val5')),
        ], style={"width": "75%",
                  "float": "right",
                  "display": "inline-block",
                  "padding-left": "75px"})
    ]),
    className="mt-3",
)

corr_tab = dbc.Card(
    dbc.CardBody([
        html.Div(
            [
                html.P(
                    ["Correlation Tests" + ":", dcc.Dropdown(id="corr-test",
                                                             options=correlation_options)]),
                html.P(
                    ["Test Variable 1" + ":", dcc.Dropdown(id="corr-var1",
                                                           options=num_options)]),
                html.P(
                    ["Test Variable 2" + ":", dcc.Dropdown(id="corr-var2",
                                                           options=num_options)])
            ],
            style={"width": "25%", "float": "left", "padding": "20px"},
        ),
        dcc.Graph(id="plot-corr", figure={}, style={"width": "75%", "display": "inline-block", "height": 500}),
        html.Table([
            html.Tr(html.Td(id='corr-val1'))
        ], style={"width": "75%",
                  "float": "right",
                  "display": "inline-block",
                  "padding-left": "75px"})
    ]),
    className="mt-3",
)

para_tab = dbc.Card(
    dbc.CardBody([
        html.Div(
            [
                html.P(
                    ["Parametric Tests" + ":", dcc.Dropdown(id="para-test",
                                                            options=parametric_options)]),
                html.P(
                    ["Test Variable 1" + ":", dcc.Dropdown(id="para-var1",
                                                           options=num_options)]),
                html.P(
                    ["Test Variable 2" + ":", dcc.Dropdown(id="para-var2",
                                                           options=num_options)]),
                # html.P(
                #     ["Test Variables" + ":", dcc.Dropdown(id="para-var3",
                #                                           options=num_options,
                #                                           multi=True)], style={'display': 'none'})
            ],
            style={"width": "25%", "float": "left", "padding": "20px"},
        ),
        dcc.Graph(id="plot-para", figure={}, style={"width": "75%", "display": "inline-block", "height": 500}),
        html.Table([
            html.Tr(html.Td(id='para-val1'))
        ], style={"width": "75%",
                  "float": "right",
                  "display": "inline-block",
                  "padding-left": "75px"})
    ]),
    className="mt-3",
)

tab_qnt_content = dbc.Card(
    dbc.CardBody(
        [
            dcc.Tabs(id="tabs-qnt", value='tab-norm', children=[
                dcc.Tab(children=norm_tab,
                        label='Normalize',
                        value='tab-norm',
                        style=tab_style,
                        selected_style=tab_selected_style),
                dcc.Tab(children=corr_tab,
                        label='Correlation',
                        value='tab-corr',
                        style=tab_style,
                        selected_style=tab_selected_style),
                dcc.Tab(children=para_tab,
                        label='Parametric',
                        value='tab-para',
                        style=tab_style,
                        selected_style=tab_selected_style)
            ], style=tabs_styles)
        ]

    ),
    className="mt-3",
)


########################################################################################################################


@app.callback(
    Output("no-data", "children"),
    [Input("input-url", "value"),
     Input("load-button", "n_clicks")])
def output_text(value, n):
    if value is not None and n is not None:
        global df_up
        # global data_name
        df_up = pd.read_csv(value)
        df_up.insert(loc=0, column=' index', value=range(1, len(df_up) + 1))
        # data_name = value.split('/')[-1].split('.')[0]
        if not df_up.empty:
            global colnames
            colnames = df_up.columns
        return df_up.to_json(date_format='iso', orient='split')


@app.callback(
    [Output('datatable', 'data'),
     Output('datatable', 'columns')],
    [Input('datatable', "page_current"),
     Input('datatable', "page_size"),
     Input('datatable', 'sort_by'),
     Input('datatable', "filter_query"),
     Input('datatable-row-count', 'value'),
     Input('no-data', 'children')])
def update_table(page_current, page_size, sort_by, filter, row_count_value, data):
    if not df_up.empty:
        # df_temp = pd.read_json(data, orient='split')
        df_tab = df_up
    else:
        df_tab = df
    if row_count_value is not None:
        page_size = row_count_value

    if len(sort_by):
        dff = df_tab.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = df_tab

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

    # if selected_cols is not None:
    #     if len(selected_cols) != 0:
    #         return dff[selected_cols].iloc[
    #                page_current * page_size:(page_current + 1) * page_size
    #                ].to_dict('records')
    #     else:
    #         return dff.iloc[
    #                page_current * page_size:(page_current + 1) * page_size
    #                ].to_dict('records')
    # else:

    dff = dff.round(2)

    return [dff.iloc[
            page_current * page_size:(page_current + 1) * page_size
            ].to_dict('records'),
            [{"name": [i, j], "id": i} for i, j in zip(df_tab.columns, [str(x) for x in df_tab.dtypes.to_list()])]]


########################################################################################################################
# @app.callback(
#     [Output("xlab-scat", "options"),
#      Output("ylab-scat", "options"),
#      Output("col-scat", "options"),
#      Output("siz-scat", "options"),
#      Output("fac-scat-row", "options"),
#      Output("fac-scat-col", "options")],
#     [Input("xlab-scat", "value")])      #################################################
# def update_scat_dd(data):
#     if not df_up.empty:
#         xlab_options = [dict(label=x, value=x) for x in df_up.columns]
#         ylab_options = [dict(label=x, value=x) for x in df_up.columns]
#         color_options = [dict(label=x, value=x) for x in df_up.columns]
#         siz_options = [dict(label=x, value=x) for x in df_up.columns]
#         fac_row_options = [dict(label=x, value=x) for x in df_up.columns]
#         fac_col_options = [dict(label=x, value=x) for x in df_up.columns]
#
#         return [xlab_options, ylab_options, color_options,
#                 siz_options, fac_row_options, fac_col_options]

# html.P(["X label" + ":", dcc.Dropdown(id="xlab-scat", options=col_options)]),
#                 html.P(["Y label" + ":", dcc.Dropdown(id="ylab-scat", options=col_options)]),
#                 html.P(["Color" + ":", dcc.Dropdown(id="col-scat", options=col_options)]),
#                 html.P(["Size" + ":", dcc.Dropdown(id="siz-scat", options=col_options)]),
#                 html.P(["Facet Row" + ":", dcc.Dropdown(id="fac-scat-row", options=col_options)]),
#                 html.P(["Facet Column" + ":", dcc.Dropdown(id="fac-scat-col", options=col_options)]),
#                 html.P(["Trendline" + ":", dcc.Dropdown(id="trnd-scat",

########################################################################################################################


@app.callback(
    Output("plot-scatter", "figure"),
    [Input("xlab-scat", "value"),
     Input("ylab-scat", "value"),
     Input("col-scat", "value"),
     Input("siz-scat", "value"),
     Input("fac-scat-row", "value"),
     Input("fac-scat-col", "value"),
     Input("trnd-scat", "value")])
def update_scatter(x, y, color, size, facet_row, facet_col, trend):
    if df_up.empty:
        return px.scatter(
            df,
            x=x,
            y=y,
            color=color,
            size=size,
            facet_row=facet_row,
            facet_col=facet_col,
            trendline=trend,
            height=700)
    elif not df_up.empty:
        return px.scatter(
            df_up,
            x=x,
            y=y,
            color=color,
            size=size,
            facet_row=facet_row,
            facet_col=facet_col,
            trendline=trend,
            height=700)


@app.callback(
    [Output('xlab-scat', 'options'),
     Output('ylab-scat', 'options'),
     Output('col-scat', 'options'),
     Output('siz-scat', 'options'),
     Output('fac-scat-row', 'options'),
     Output('fac-scat-col', 'options')],
    [Input('load-button-scat', 'n_clicks')])
def update_labs(n):
    if n is not None:
        return [[{'label': i, 'value': i} for i in colnames],
                [{'label': i, 'value': i} for i in colnames],
                [{'label': i, 'value': i} for i in colnames],
                [{'label': i, 'value': i} for i in colnames],
                [{'label': i, 'value': i} for i in colnames],
                [{'label': i, 'value': i} for i in colnames]]
    else:
        return [[{'label': i, 'value': i} for i in col_options],
                [{'label': i, 'value': i} for i in col_options],
                [{'label': i, 'value': i} for i in col_options],
                [{'label': i, 'value': i} for i in col_options],
                [{'label': i, 'value': i} for i in col_options],
                [{'label': i, 'value': i} for i in col_options], ]


@app.callback(
    Output("plot-bar", "figure"),
    [Input("xlab-bar", "value"),
     Input("ylab-bar", "value"),
     Input("col-bar", "value"),
     Input("typ-bar", "value"),
     Input("fac-bar-row", "value"),
     Input("fac-bar-col", "value")])
def update_bar(x, y, color, type, facet_row, facet_col):
    if df_up.empty:
        return px.bar(
            df,
            x=x,
            y=y,
            color=color,
            facet_row=facet_row,
            facet_col=facet_col,
            height=700)
    else:
        return px.bar(
            df_up,
            x=x,
            y=y,
            color=color,
            facet_row=facet_row,
            facet_col=facet_col,
            height=700)


@app.callback(
    [Output('xlab-bar', 'options'),
     Output('ylab-bar', 'options'),
     Output('col-bar', 'options'),
     Output('fac-bar-row', 'options'),
     Output('fac-bar-col', 'options')],
    [Input('load-button-bar', 'n_clicks')])
def update_labs(n):
    if n is not None:
        return [[{'label': i, 'value': i} for i in colnames],
                [{'label': i, 'value': i} for i in colnames],
                [{'label': i, 'value': i} for i in colnames],
                [{'label': i, 'value': i} for i in colnames],
                [{'label': i, 'value': i} for i in colnames]]
    else:
        return [[{'label': i, 'value': i} for i in col_options],
                [{'label': i, 'value': i} for i in col_options],
                [{'label': i, 'value': i} for i in col_options],
                [{'label': i, 'value': i} for i in col_options],
                [{'label': i, 'value': i} for i in col_options]]


@app.callback(
    Output("plot-box", "figure"),
    [Input("xlab-box", "value"),
     Input("ylab-box", "value"),
     Input("col-box", "value"),
     Input("fac-box-row", "value"),
     Input("fac-box-col", "value")])
def update_box(x, y, color, facet_row, facet_col):
    if df_up.empty:
        return px.box(
            df,
            x=x,
            y=y,
            color=color,
            facet_row=facet_row,
            facet_col=facet_col,
            height=700)
    else:
        return px.box(
            df_up,
            x=x,
            y=y,
            color=color,
            facet_row=facet_row,
            facet_col=facet_col,
            height=700)


@app.callback(
    [Output('xlab-box', 'options'),
     Output('ylab-box', 'options'),
     Output('col-box', 'options'),
     Output('fac-box-row', 'options'),
     Output('fac-box-col', 'options')],
    [Input('load-button-box', 'n_clicks')])
def update_labs(n):
    if n is not None:
        return [[{'label': i, 'value': i} for i in colnames],
                [{'label': i, 'value': i} for i in colnames],
                [{'label': i, 'value': i} for i in colnames],
                [{'label': i, 'value': i} for i in colnames],
                [{'label': i, 'value': i} for i in colnames]]
    else:
        return [[{'label': i, 'value': i} for i in col_options],
                [{'label': i, 'value': i} for i in col_options],
                [{'label': i, 'value': i} for i in col_options],
                [{'label': i, 'value': i} for i in col_options],
                [{'label': i, 'value': i} for i in col_options]]


@app.callback(
    Output("plot-heat", "figure"),
    [Input("xlab-heat", "value"),
     Input("ylab-heat", "value"),
     Input("fac-heat-row", "value"),
     Input("fac-heat-col", "value")])
def update_heatmap(x, y, facet_row, facet_col):
    if df_up.empty:
        return px.density_heatmap(
            df,
            x=x,
            y=y,
            facet_row=facet_row,
            facet_col=facet_col,
            height=700)
    else:
        return px.density_heatmap(
            df_up,
            x=x,
            y=y,
            facet_row=facet_row,
            facet_col=facet_col,
            height=700)


@app.callback(
    [Output('xlab-heat', 'options'),
     Output('ylab-heat', 'options'),
     Output('fac-heat-row', 'options'),
     Output('fac-heat-col', 'options')],
    [Input('load-button-heat', 'n_clicks')])
def update_labs(n):
    if n is not None:
        return [[{'label': i, 'value': i} for i in colnames],
                [{'label': i, 'value': i} for i in colnames],
                [{'label': i, 'value': i} for i in colnames],
                [{'label': i, 'value': i} for i in colnames]]
    else:
        return [[{'label': i, 'value': i} for i in col_options],
                [{'label': i, 'value': i} for i in col_options],
                [{'label': i, 'value': i} for i in col_options],
                [{'label': i, 'value': i} for i in col_options]]


# @app.callback(
#     Output('no-data-plt', 'children'),
#     [Input('url', 'pathname')])
# def update_hidden_div(url_path):
#     if url_path == '/apps/plt':
#         return colnames
#
#
# @app.callback(
#     Output('xlab-scat', 'options'),
#     [Input('no-data-plt', 'children')])
# def update_scat_x_dropdown(col_names):
#     if df_up.empty:
#         options = [{'label': i, 'value': i} for i in colnames]
#         return {'options': options}
#     elif not df_up.empty:
#         options = [{'label': i, 'value': i} for i in colnames]
#         return {'options': options}

########################################################################################################################


# @app.callback(
#     Output("plot-bar", "figure"),
#     [Input("xlab-bar", "value"),
#      Input("ylab-bar", "value"),
#      Input("col-bar", "value"),
#      Input("typ-bar", "value"),
#      Input("fac-bar-row", "value"),
#      Input("fac-bar-col", "value")])
# def update_bar(x, y, color, type, facet_row, facet_col):
#     return px.bar(
#         df,
#         x=x,
#         y=y,
#         color=color,
#         facet_row=facet_row,
#         facet_col=facet_col,
#         height=700,
#     )


# @app.callback(
#     Output("plot-box", "figure"),
#     [Input("xlab-box", "value"),
#      Input("ylab-box", "value"),
#      Input("col-box", "value"),
#      Input("fac-box-row", "value"),
#      Input("fac-box-col", "value")])
# def update_box(x, y, color, facet_row, facet_col):
#     return px.box(
#         df,
#         x=x,
#         y=y,
#         color=color,
#         facet_row=facet_row,
#         facet_col=facet_col,
#         height=700,
#     )


# @app.callback(
#     Output("plot-heat", "figure"),
#     [Input("xlab-heat", "value"),
#      Input("ylab-heat", "value"),
#      Input("fac-heat-row", "value"),
#      Input("fac-heat-col", "value")])
# def update_heatmap(x, y, facet_row, facet_col):
#     return px.density_heatmap(
#         df,
#         x=x,
#         y=y,
#         facet_row=facet_row,
#         facet_col=facet_col,
#         height=700,
#     )


@app.callback(
    [Output("plot-norm", "figure"),
     Output("norm-val1", "children"),
     Output("norm-val2", "children"),
     Output("norm-val3", "children"),
     Output("norm-val4", "children"),
     Output("norm-val5", "children")],
    [Input("norm-test", "value"),
     Input("norm-var", "value")])
def update_norm(test, var):
    if test == "Shapiro-Wilk" and var is not None:
        stat, p = shapiro(df[var])
        fig = px.histogram(df, x=var, height=500)
        if p > 0.05:
            result1 = 'Probably Gaussian : stat=%.3f, p=%.3f' % (stat, p)
            result2 = ""
            result3 = ""
            result4 = ""
            result5 = ""
            return fig, result1, result2, result3, result4, result5
        else:
            result1 = 'Probably not Gaussian : stat=%.3f, p=%.3f' % (stat, p)
            result2 = ""
            result3 = ""
            result4 = ""
            result5 = ""
            return fig, result1, result2, result3, result4, result5

    elif test == "D’Agostino’s K^2" and var is not None:
        stat, p = normaltest(df[var])
        fig = px.histogram(df, x=var, height=500)
        if p > 0.05:
            result1 = 'Probably Gaussian : stat=%.3f, p=%.3f' % (stat, p)
            result2 = ""
            result3 = ""
            result4 = ""
            result5 = ""
            return fig, result1, result2, result3, result4, result5
        else:
            result1 = 'Probably not Gaussian : stat=%.3f, p=%.3f' % (stat, p)
            result2 = ""
            result3 = ""
            result4 = ""
            result5 = ""
            return fig, result1, result2, result3, result4, result5

    elif test == "Anderson-Darling" and var is not None:
        res = anderson(df[var])
        fig = px.histogram(df, x=var, height=500)

        if res.statistic < res.critical_values[0]:
            result1 = 'Probably Gaussian at the %.1f%% level,' % res.significance_level[0]
        else:
            result1 = 'Probably not Gaussian at the %.1f%% level,' % res.significance_level[0]
        if res.statistic < res.critical_values[1]:
            result2 = 'Probably Gaussian at the %.1f%% level,' % res.significance_level[1]
        else:
            result2 = 'Probably not Gaussian at the %.1f%% level,' % res.significance_level[1]
        if res.statistic < res.critical_values[2]:
            result3 = 'Probably Gaussian at the %.1f%% level,' % res.significance_level[2]
        else:
            result3 = 'Probably not Gaussian at the %.1f%% level,' % res.significance_level[2]
        if res.statistic < res.critical_values[3]:
            result4 = 'Probably Gaussian at the %.1f%% level,' % res.significance_level[3]
        else:
            result4 = 'Probably not Gaussian at the %.1f%% level,' % res.significance_level[3]
        if res.statistic < res.critical_values[4]:
            result5 = 'Probably Gaussian at the %.1f%% level,' % res.significance_level[4]
        else:
            result5 = 'Probably not Gaussian at the %.1f%% level,' % res.significance_level[4]
    return fig, result1, result2, result3, result4, result5


@app.callback(
    [Output("plot-corr", "figure"),
     Output("corr-val1", "children")],
    [Input("corr-test", "value"),
     Input("corr-var1", "value"),
     Input("corr-var2", "value")])
def update_corr(test, var1, var2):
    if test == "Pearson" and var1 is not None and var2 is not None:
        stat, p = pearsonr(df[var1], df[var2])
        fig = px.scatter(df, x=var1, y=var2, height=500)
        if p > 0.05:
            result1 = 'Probably independent : stat=%.3f, p=%.3f' % (stat, p)
            return fig, result1
        else:
            result1 = 'Probably dependent : stat=%.3f, p=%.3f' % (stat, p)
            return fig, result1

    elif test == "Spearman" and var1 is not None and var2 is not None:
        stat, p = spearmanr(df[var1], df[var2])
        fig = px.scatter(df, x=var1, y=var2, height=500)
        if p > 0.05:
            result1 = 'Probably independent : stat=%.3f, p=%.3f' % (stat, p)
            return fig, result1
        else:
            result1 = 'Probably dependent : stat=%.3f, p=%.3f' % (stat, p)
            return fig, result1

    elif test == "Kendall" and var1 is not None and var2 is not None:
        stat, p = kendalltau(df[var1], df[var2])
        fig = px.scatter(df, x=var1, y=var2, height=500)
        if p > 0.05:
            result1 = 'Probably independent : stat=%.3f, p=%.3f' % (stat, p)
            return fig, result1
        else:
            result1 = 'Probably dependent : stat=%.3f, p=%.3f' % (stat, p)
            return fig, result1

    elif test == "Chi-Squared" and var1 is not None and var2 is not None:
        stat, p, dof, expected = chi2_contingency(df[[var1, var2]])
        fig = px.scatter(df, x=var1, y=var2, height=500)
        if p > 0.05:
            result1 = 'Probably independent : stat=%.3f, p=%.3f' % (stat, p)
            return fig, result1
        else:
            result1 = 'Probably dependent : stat=%.3f, p=%.3f' % (stat, p)
            return fig, result1


########################################################################################################################


# @app.callback(
#     [Output("para-var1", "style"),
#      Output("para-var2", "style"),
#      Output("para-var3", "style")],
#     [Input("para-test", "value")])
# def update_display_setting(tab_val):
#     if tab_val == "Student t-test":
#         return dsp_yes, dsp_yes, dsp_no
#     elif tab_val == "Paired Student t-test":
#         return dsp_yes, dsp_yes, dsp_no
#     elif tab_val == "ANOVA":
#         return dsp_no, dsp_no, dsp_yes


@app.callback(
    [Output("plot-para", "figure"),
     Output("para-val1", "children")],
    [Input("para-test", "value"),
     Input("para-var1", "value"),
     Input("para-var2", "value")])
def update_para(test, var1, var2):
    if test == "Student t-test" and var1 is not None and var2 is not None:
        stat, p = ttest_ind(df[var1], df[var2])
        df_sub = df[[' index', var1, var2]]
        df_melt = pd.melt(df_sub, id_vars=' index')
        fig = px.histogram(df_melt, x='value', color='variable', height=500)
        if p > 0.05:
            result1 = 'Probably the same distribution : stat=%.3f, p=%.3f' % (stat, p)
            return fig, result1
        else:
            result1 = 'Probably different distributions : stat=%.3f, p=%.3f' % (stat, p)
            return fig, result1
    elif test == "Paired Student t-test" and var1 is not None and var2 is not None:
        stat, p = ttest_rel(df[var1], df[var2])
        df_sub = df[[' index', var1, var2]]
        df_melt = pd.melt(df_sub, id_vars=' index')
        fig = px.histogram(df_melt, x='value', color='variable', height=500)
        if p > 0.05:
            result1 = 'Probably the same distribution : stat=%.3f, p=%.3f' % (stat, p)
            return fig, result1
        else:
            result1 = 'Probably different distributions : stat=%.3f, p=%.3f' % (stat, p)
            return fig, result1
    elif test == "ANOVA" and var1 is not None and var2 is not None:
        stat, p = f_oneway(df[var1], df[var2])
        df_sub = df[[' index', var1, var2]]
        df_melt = pd.melt(df_sub, id_vars=' index')
        fig = px.histogram(df_melt, x='value', color='variable', height=500)
        if p > 0.05:
            result1 = 'Probably the same distribution : stat=%.3f, p=%.3f' % (stat, p)
            return fig, result1
        else:
            result1 = 'Probably different distributions : stat=%.3f, p=%.3f' % (stat, p)
            return fig, result1


app.run_server(debug=False)
