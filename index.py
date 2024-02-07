# index.py
from dash import Dash, dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc
from app import app
import inventor_page  # The code you provided goes here, but refactored as a layout in a separate file
import main_page
import applicants_page
import applicants_countries_page
import jurisdiction_page

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    # html.Div(id='page-content'),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/inventor':
        return inventor_page.layout
    elif pathname == '/applicants':
        return applicants_page.layout
    elif pathname == '/applicants_countries':
        return applicants_countries_page.layout
    elif pathname == '/jurisdiction':
        return jurisdiction_page.layout
    else:
        return main_page.layout






if __name__ == '__main__':
    app.run_server(debug=True)
