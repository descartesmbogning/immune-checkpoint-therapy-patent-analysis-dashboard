# Import required libraries
from components import Navbar, Footer
from dash import dcc, html, Input, Output, dash_table, callback, State, callback_context, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
import numpy as np
from dash.dash_table.Format import Format, Scheme
from dash.dependencies import Input, Output
import json  # Import json for parsing clickData

# Load your data
df = pd.read_csv('./data/inventor_table.csv')
df_trend = pd.read_csv('./data/inventor_year_table.csv')

# Drop 'Unnamed: 0' column if it exists
if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])

# Define helper functions for dynamic content (Placeholder content for now)
def get_total_inventors():
    return str(df['Inventor'].count())

# def get_top_inventor():
#     return df['Inventor'].value_counts().idxmax()

# Layout for the inventor page
layout = dbc.Container([
    Navbar(),  # Include navbar at the top
    dbc.Row(dbc.Col(html.H1("Inventors"), width={'size': 6, 'offset': 3}, className="text-center mt-1 mb-2")),
    dbc.Row([
        dbc.Col(html.P("According to lens.org, an inventor is a person who made an inventive contribution to the invention as defined by the claims of the patent application."), width={'size': 10, 'offset': 0}, className="d-flex justify-content-center"),
        dbc.Col(html.P("Explore the contributions of key inventors in the field of immune checkpoint therapy."), width={'size': 10, 'offset': 0}, className="d-flex justify-content-center"),
        dbc.Col(html.P("Use the table below to sort, filter, and understand the landscape of patent contributions."), width={'size': 10, 'offset': 0}, className="d-flex justify-content-center")
        ], className="mb-2 d-flex justify-content-center"
    ),  
     # Key Metrics in Cards
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total Inventors", className="card-title"),
                html.P(get_total_inventors(), className="card-text")
            ])
        ]), className="text-center mt-1 mb-1", width=4),
        # dbc.Col(dbc.Card([
        #     dbc.CardBody([
        #         html.H5("Top Inventor", className="card-title"),
        #         html.P(get_top_inventor(), className="card-text")
        #     ])
        # ]), width=4),
        # # ... Add more cards as needed ...
    ], className="mb-2 d-flex justify-content-center"),

    # Buttons for downloading data
    dbc.Row([
        dbc.Col(html.Button("Download Full Data", id="btn_download_full_inventor"), width={'size': 2, 'offset': 0}),
        dbc.Col(html.Button("Download Selected Data", id="btn_download_selected_inventor"), width=2),
    ], justify="start", className="mb-0"),
    
    # Data Table
    dash_table.DataTable(
        id='inventor-datatable-interactivity',
        columns=[
            {
                "name": f"{i} (use: >, <, =)" if df[i].dtype in [np.float64, np.int64] else i,
                "id": i,
                "type": "numeric",
                "format": Format(precision=4, scheme=Scheme.decimal_or_exponent) if df[i].dtype in [np.float64, np.int64] else None
            } for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        page_action="native",
        page_current= 0,
        page_size= 10,
        style_table={'height': '400px', 'overflowY': 'auto'},
        style_cell={
            'height': 'auto',
            'minWidth': '80px', 'width': '120px', 'maxWidth': '180px',
            'whiteSpace': 'normal'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
    ),

    # Place the metric dropdown right above the Data Table
    dbc.Row(
        [
            dbc.Col(html.Label("Select Metric:"), width=2),
            dbc.Col(
                dcc.Dropdown(
                    id='inventor-metric-dropdown',
                    options=[
                        {'label': 'Patent Count', 'value': 'Patent Count'},
                        {'label': 'Total Citations', 'value': 'Total Citations'},
                        {'label': 'Degree Centrality', 'value': 'Degree Centrality'},
                        {'label': 'Betweenness Centrality', 'value': 'Betweenness Centrality'},
                        {'label': 'Duration (Years)', 'value': 'Duration (Years)'}
                    ],
                    value='Patent Count'  # default value
                ),
                width=3
            ),
        ],
        className="mb-0  d-flex justify-content-center"
    ),
    
    # Bar Chart
    dbc.Row(dbc.Col(dcc.Graph(id='inventor-bar-chart'), width=12)),
    
    # Line Chart
    dbc.Row(dbc.Col(dcc.Graph(id='inventor-line-chart'), width=12)),


    dbc.Row([
        dbc.Col(dcc.Link(
            html.Div([
                html.Img(src='/assets/inventor_VOSviewer-screenshot.png', style={'max-width': '100%', 'max-height': '600px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}),
                # html.P("Inventors")
            ]),
            target='_blank',  # Opens the link in a new tab
            href='http://tinyurl.com/2cuh8nca'
        ), width={"size": 8, "offset": 1}, className="d-flex justify-content-center mt-5 mb-5"),  
    ], className="mb-2 d-flex justify-content-center"),

    # dbc.Row(
    #     dbc.Col(
    #         html.Iframe(
    #             src="http://tinyurl.com/2cuh8nca",
    #             style={
    #                 "border": "1px solid #ddd",
    #                 "width": "100%",  # Adjust width as needed
    #                 "height": "500px",  # Adjust height as needed
    #                 "display": "block",
    #                 "margin-left": "auto",
    #                 "margin-right": "auto"
    #             },
    #             allow="fullscreen",  # This enables fullscreen mode
    #         ),
    #         width=12,  # Adjust the column width as needed
    #     )
    # ),



    # Hidden Divs for JSON-serialized data
    html.Div(id='inventor-data-storage-full', style={'display': 'none'}),
    html.Div(id='inventor-data-storage-selected', style={'display': 'none'}),
    # Add this Div to your layout where you want to display the inventor details
    html.Div(id='inventor-details-container'),

    # Hidden element for triggering downloads
    dcc.Download(id="inventor-download-dataframe-csv"),

    Footer()  # Include footer at the bottom

], fluid=True)

# Callbacks for the Inventor page

@callback(
    Output('inventor-bar-chart', 'figure'),
    [Input('inventor-datatable-interactivity', 'derived_virtual_data'),
     Input('inventor-datatable-interactivity', 'derived_virtual_selected_rows'),
     Input('inventor-metric-dropdown', 'value')]  # Input from the dropdown
)
def update_inventor_bar_chart(rows, derived_virtual_selected_rows, selected_metric):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    # When the table is first loaded and there's no filtering or sorting, use original data
    dff = pd.DataFrame(rows) if rows is not None else df

    if len(derived_virtual_selected_rows) == 0:
        # Sort the DataFrame by the selected metric and take the top 20
        filtered_df = dff.sort_values(selected_metric, ascending=False).head(20)
        title = f'Top 20 Inventors by {selected_metric}'
    else:
        filtered_df = dff.iloc[derived_virtual_selected_rows]
        # Even when specific inventors are selected, sort them by the selected metric
        filtered_df = filtered_df.sort_values(selected_metric, ascending=False)
        title = f'Selected Inventors by {selected_metric}'

    # Plotting the bar chart
    # fig = px.bar(filtered_df, x="Inventor", y=selected_metric, color="2023 Classification", barmode="group",
    #              category_orders={"Inventor": filtered_df["Inventor"].tolist()})  # Ensure consistent ordering
    # fig.update_layout(title=title)

    fig = px.bar(filtered_df, x="Inventor", y=selected_metric, color="2023 Classification",
             hover_data=[selected_metric, 'First Year', 'Last Year','Mean Patents/Year'],
             barmode="group",
             category_orders={"Inventor": filtered_df["Inventor"].tolist()})  # Ensure consistent ordering
             
    fig.update_traces(hovertemplate="Inventor: %{x}<br>" + selected_metric + ": %{y}<br>First Year: %{customdata[0]}<br>Last Year: %{customdata[1]}<br>Mean Patents/Year: %{customdata[2]}")
    fig.update_layout(title=title)
    return fig

# ...
@callback(
    Output('inventor-details', 'children'),  # 'inventor-details' is an id for a Div where you want to display more info
    [Input('inventor-bar-chart', 'clickData')]  # 'inventor-bar-chart' is the id of your bar chart
)
def display_click_data(clickData):
    if clickData is None:
        raise PreventUpdate
    inventor_name = clickData['points'][0]['x']
    # Assuming you have a function to get details based on inventor name
    details = get_inventor_details(inventor_name)  
    return html.P(details)

# You'll need to create a Div with the id 'inventor-details' in your layout to display the details.

#####
@callback(
    Output('inventor-line-chart', 'figure'),
    [Input('inventor-datatable-interactivity', 'derived_virtual_data'),  # Get the filtered data from the table
     Input('inventor-datatable-interactivity', 'derived_virtual_selected_rows'),  # Get the selected rows from the table
     Input('inventor-bar-chart', 'clickData')]  # Get the click data from the bar chart
)
def update_inventor_line_chart(all_rows_data, slctd_row_indices, clickData):
    # Process the data from the table
    dff = pd.DataFrame(all_rows_data) if all_rows_data is not None else pd.DataFrame()
    selected_inventors = dff.iloc[slctd_row_indices]['Inventor'].tolist() if slctd_row_indices else []

    # Process the click data from the bar chart
    if clickData:
        clicked_inventor = clickData['points'][0]['x']
        if clicked_inventor not in selected_inventors:
            selected_inventors.append(clicked_inventor)

    # Aggregate data: count patents per year for each inventor
    inventor_yearly_counts = df_trend.groupby(['Application Year', 'Inventor']).size().reset_index(name='Patent Count')

    # Create the line chart
    if selected_inventors:
        filtered_df = inventor_yearly_counts[inventor_yearly_counts['Inventor'].isin(selected_inventors)]
        fig = px.line(filtered_df, x='Application Year', y='Patent Count', color='Inventor',markers=True)
        fig.update_layout(title='Contribution Trends of Selected Inventors Over Years')
    else:
        # When no inventors are selected, show the global trend
        df_trend2 = df_trend[['Lens ID','Application Year']].drop_duplicates()
        global_yearly_counts = df_trend2.groupby(['Application Year']).size().reset_index(name='Total Patents')
        fig = px.line(global_yearly_counts, x='Application Year', y='Total Patents',markers=True)
        fig.update_layout(title='Global Trend of Patent Contributions Over Years')
    
    return fig


@callback(
    [Output('inventor-data-storage-full', 'children'),
     Output('inventor-data-storage-selected', 'children')],
    [Input('inventor-datatable-interactivity', 'derived_virtual_data'),
     Input('inventor-datatable-interactivity', 'derived_virtual_selected_rows')]
)
def store_inventor_data(all_rows_data, slctd_row_indices):
    if all_rows_data is None:
        raise PreventUpdate
    
    # Store full data
    full_data_str = pd.DataFrame(all_rows_data).to_json(date_format='iso', orient='split')

    # Store selected data
    if slctd_row_indices is None or len(slctd_row_indices) == 0:
        selected_data_str = None
    else:
        selected_data_str = pd.DataFrame([all_rows_data[i] for i in slctd_row_indices]).to_json(date_format='iso', orient='split')
    
    return full_data_str, selected_data_str

@callback(
    Output("inventor-download-dataframe-csv", "data"),
    [Input("btn_download_full_inventor", "n_clicks"),
     Input("btn_download_selected_inventor", "n_clicks"),
     Input('inventor-data-storage-full', 'children'),
     Input('inventor-data-storage-selected', 'children')],
    prevent_initial_call=True,
)
def download_inventor_csv(btn_full_inventor, btn_selected_inventor, full_data_str, selected_data_str):
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == "btn_download_full_inventor":
        df = pd.read_json(full_data_str, orient='split')
        return dcc.send_data_frame(df.to_csv, filename="full_data_inventor.csv")
    elif button_id == "btn_download_selected_inventor":
        if selected_data_str:
            df = pd.read_json(selected_data_str, orient='split')
            return dcc.send_data_frame(df.to_csv, filename="selected_data_inventor.csv")
    return no_update

if __name__ == '__main__':
    app.run_server(debug=True)
