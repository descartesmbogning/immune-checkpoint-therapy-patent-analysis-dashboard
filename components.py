
import dash_bootstrap_components as dbc
from dash import dcc, html

# def Navbar():
#     navbar = dbc.NavbarSimple(
#         children=[
#             dbc.NavItem(dcc.Link('Home', href='/', className='nav-link')),
#             dbc.NavItem(dcc.Link('Inventors', href='/inventor', className='nav-link')),
#             dbc.NavItem(dcc.Link('Applicants', href='/applicants', className='nav-link')),
#             dbc.NavItem(dcc.Link('Applicant countries', href='/applicants_countries', className='nav-link')),
#             dbc.NavItem(dcc.Link('Jurisdictions', href='/jurisdiction', className='nav-link')),
#         ],
#         brand="Immune Checkpoint Therapy Patent Analysis",
#         brand_href="/",
#         color="primary",
#         dark=True,
#         className="mb-4"
#     )
#     return navbar

# def Footer():
#     footer = html.Footer(
#         dbc.Container(
#             dbc.Row(
#                 dbc.Col(
#                     html.Small("Data Source: Lens.org | Last Updated: 28/01/2024 | By Maxime Descartes Mbogning"), 
#                     className="text-center"
#                 )
#             )
#         ),
#         className="footer mt-auto py-3 bg-light"
#     )
#     return footer


# components.py
import dash_bootstrap_components as dbc
from dash import dcc, html

def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dcc.Link([
                    html.I(className="fas fa-home mr-1"),  # FontAwesome icon
                    "Home"
                ], href='/', className='nav-link')),
            dbc.NavItem(dcc.Link('Inventors', href='/inventor', className='nav-link')),
            dbc.NavItem(dcc.Link('Applicants', href='/applicants', className='nav-link')),
            dbc.NavItem(dcc.Link('Applicant countries', href='/applicants_countries', className='nav-link')),
            dbc.NavItem(dcc.Link('Jurisdictions', href='/jurisdiction', className='nav-link')),
            # Language selection dropdown
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("English", id="lang-english"),
                    dbc.DropdownMenuItem("Français", id="lang-french"),
                    # Add more languages as needed
                ],
                nav=True,
                in_navbar=True,
                label="Language",
                id="language-dropdown",
                
            ),
        ],
        brand="Immune Checkpoint Therapy Patent Analysis",
        brand_href="/",
        color="primary",
        dark=True,
        className="mb-4 sticky-navbar",  # Add the sticky-navbar class
        # className="mb-4",
        sticky="top",
        style={"box-shadow": "0 2px 4px rgba(0,0,0,.1)"},  # Add a subtle shadow
    )
    return navbar

# To make the navbar sticky, use a style or className with appropriate CSS
navbar_container = html.Div(
    Navbar,
    style={'position': 'sticky', 'top': 0, 'zIndex': 1020}  # Ensure it's above other content
)


def Footer():
    footer = html.Footer(
        dbc.Container(
            dbc.Row(
                dbc.Col(
                    html.Small("Data Source: Lens.org | Last Updated: 28/01/2024 | By Maxime Descartes Mbogning"), 
                    className="text-center"
                )
            )
        ),
        className="footer mt-auto py-3 bg-light"
    )
    return footer
