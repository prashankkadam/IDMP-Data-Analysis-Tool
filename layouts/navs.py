# -*- coding:/ utf-8 -*-
"""
This piece of software is bound by The MIT License (MIT)
Copyright (c) 2019 Prashank Kadam
Code written by : Prashank Kadam
User name - ADM-PKA187
Email ID : prashank.kadam@maersktankers.com
Created on - Fri Aug 16 15:20:33 2019
version : 1.0
"""
# Importing the required libraries
import dash_html_components as html
import dash_bootstrap_components as dbc
import base64

# In this file, we set the complete layout for the navigation bar and the nav toggles

# Setting the global names for Maersk logo and the encoded image directory
MAERSK_LOGO = 'maersk_logo.jpg'
ENCODED_URL = 'data:image/png;base64,{}'

# Encoding the Maersk logo
logo_enc = base64.b64encode(open(MAERSK_LOGO, 'rb').read())

# Setting the layout for the navbar:
navbar = html.Div([
    dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=ENCODED_URL.format(logo_enc.decode()), height="60px")),
                        # dbc.Col(dbc.NavbarBrand("IMO 2020", className="ml-2"), style={'font-weight':'bold'}),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/apps/rob",
            ),
            dbc.NavbarToggler(id="navbar-toggler")
        ],
    )
])

# # Setting the layout for navs and formatting the CSS layouts
# nav = html.Div([
#     dbc.Nav(
#         [
#             dbc.NavLink("ROB", id="id_rob", href="/apps/rob", style={'min-width': '200px', 'color': 'skyblue'}),
#             dbc.NavLink("Monthly Consumption", id="id_mon", href="/apps/monthly",
#                         style={'min-width': '250px', 'color': 'skyblue'}),
#             # dbc.NavLink("Bunkers", id="id_bun", href="/apps/bunker", style={'min-width': '300px',  'color': 'skyblue'}),
#             # dbc.NavLink("Disabled", disabled=True, href="#", style={'min-width': '200px', 'color': 'skyblue'}),
#         ],
#         id='id_nav'
#     )
# ], style={'padding-bottom': '10px', 'padding-left': '50px', 'font-weight': 'bold', 'line-height': '60px',
#           'font-size': '25px'})
