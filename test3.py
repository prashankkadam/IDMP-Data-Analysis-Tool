import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output
import pandas as pd

# Statmodels installation required for trendline

df = pd.read_csv('data/bcw.csv')

df[' index'] = range(1, len(df) + 1)

colnames = df.columns
dtype_mapping = dict(df.dtypes)
numeric_cols = [c for c in colnames if dtype_mapping[c] != 'O']
catagory_cols = [c for c in colnames if dtype_mapping[c] == 'O']

PAGE_SIZE = 15
dimensions = ["x", "y", "color", "facet_col", "facet_row"]
graph_types = ["Scatter", "Bar", "Box", "Heatmap"]
hypothesis_tests = ["Normality", "Correlation", "Parametric"]
normality_tests = ["Shapiro-Wilk", "D’Agostino’s K^2", "Anderson-Darling"]
correlation_tests = ["Pearson", "Spearman", "Kendall", "Chi-Squared"]
parametric_tests = ["Student t-test", "Paired Student t-test", "ANOVA", "Repeated ANOVA"]

col_options = [dict(label=x, value=x) for x in df.columns]
num_options = [dict(label=x, value=x) for x in list(set(numeric_cols))]
cat_options = [dict(label=x, value=x) for x in list(set(catagory_cols))]
graph_options = [dict(label=x, value=x) for x in graph_types]

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
    'backgroundColor': 'skyblue',
    'color': 'white',
    'padding': '6px'
}

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(
    __name__, external_stylesheets=external_stylesheets
)

app.config.suppress_callback_exceptions = True

nav = html.Div([
    dbc.Nav(
        [
            dbc.NavLink("Data Table",
                        id="id_dat",
                        href="/apps/dat",
                        style={'min-width': '200px', 'color': 'skyblue'}),
            dbc.NavLink("Plot",
                        id="id_plt",
                        href="/apps/plt",
                        style={'min-width': '200px', 'color': 'skyblue'}),
            dbc.NavLink("Quantization",
                        id="id_qnt",
                        href="/apps/qnt",
                        style={'min-width': '200px', 'color': 'skyblue'}),
            # dbc.NavLink("Disabled", disabled=True, href="#", style={'min-width': '200px', 'color': 'skyblue'}),
        ],
        id='id_nav'
    )
], style={'padding-left': '50px', 'font-weight': 'bold', 'line-height': '30px',
          'font-size': '20px'})

app.layout = html.Div([
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
    # elif pathname == '/apps/bunker':
    #     return scat_tab
    else:
        return tab_data_content


########################################################################################################################
tab_data_content = dbc.Card(
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
        html.P(["Row Count" + ":", dcc.Input(id="datatable-row-count",
                                             type='number',
                                             value=15)],
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
            ], style=tabs_styles)
        ]

    ),
    className="mt-3",
)


########################################################################################################################


@app.callback(
    Output('datatable', 'data'),
    [Input('datatable', "page_current"),
     Input('datatable', "page_size"),
     Input('datatable', 'sort_by'),
     Input('datatable', "filter_query"),
     Input('datatable-row-count', 'value')])
def update_table(page_current, page_size, sort_by, filter, row_count_value):
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

    return dff.iloc[
           page_current * page_size:(page_current + 1) * page_size
           ].to_dict('records')


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
    return px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        size=size,
        facet_row=facet_row,
        facet_col=facet_col,
        trendline=trend,
        height=700,
    )


@app.callback(
    Output("plot-bar", "figure"),
    [Input("xlab-bar", "value"),
     Input("ylab-bar", "value"),
     Input("col-bar", "value"),
     Input("typ-bar", "value"),
     Input("fac-bar-row", "value"),
     Input("fac-bar-col", "value")])
def update_bar(x, y, color, type, facet_row, facet_col):
    return px.bar(
        df,
        x=x,
        y=y,
        color=color,
        facet_row=facet_row,
        facet_col=facet_col,
        height=700,
    )


@app.callback(
    Output("plot-box", "figure"),
    [Input("xlab-box", "value"),
     Input("ylab-box", "value"),
     Input("col-box", "value"),
     Input("fac-box-row", "value"),
     Input("fac-box-col", "value")])
def update_bar(x, y, color, facet_row, facet_col):
    return px.box(
        df,
        x=x,
        y=y,
        color=color,
        facet_row=facet_row,
        facet_col=facet_col,
        height=700,
    )


@app.callback(
    Output("plot-heat", "figure"),
    [Input("xlab-heat", "value"),
     Input("ylab-heat", "value"),
     Input("fac-heat-row", "value"),
     Input("fac-heat-col", "value")])
def update_bar(x, y, facet_row, facet_col):
    return px.density_heatmap(
        df,
        x=x,
        y=y,
        facet_row=facet_row,
        facet_col=facet_col,
        height=700,
    )


########################################################################################################################
app.run_server(debug=True)
