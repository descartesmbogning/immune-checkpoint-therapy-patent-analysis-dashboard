import dash
from dash import Dash
import dash_bootstrap_components as dbc

# app = Dash(__name__, suppress_callback_exceptions=True)

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
server = app.server  # the Flask app
