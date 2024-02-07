# Import required libraries
from components import Navbar, Footer
from dash import dcc, html, Input, Output, dash_table, callback, State, callback_context, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
import numpy as np
from dash.dash_table.Format import Format, Scheme

# Load your data
df = pd.read_csv('./data/applicant_country_table.csv')
df_trend = pd.read_csv('./data/applicant_country_year_table.csv')

# Drop 'Unnamed: 0' column if it exists
if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])

# Define helper functions for dynamic content (Placeholder content for now)
def get_total_applicant_country():
    return str(df['Applicant country'].count())

# Layout for the applicant countries page
layout = dbc.Container([
    Navbar(),  # Include navbar at the top
    dbc.Row(dbc.Col(html.H1("Applicant countries"), width={'size': 6, 'offset': 3}, className="text-center mt-1 mb-2")),
   
     dbc.Row([
        dbc.Col(html.P("The applicant countries refer to the nations where the applicants originate from."), width={'size': 10, 'offset': 0}, className="d-flex justify-content-center"),
        dbc.Col(html.P("Explore the contributions of key inventors in the field of immune checkpoint therapy."), width={'size': 10, 'offset': 0}, className="d-flex justify-content-center"),
        dbc.Col(html.P("Use the table below to sort, filter, and understand the landscape of patent contributions."), width={'size': 10, 'offset': 0}, className="d-flex justify-content-center")
        ], className="mb-2 d-flex justify-content-center"
    ),     
     # Key Metrics in Cards
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total Countries", className="card-title"),
                html.P(get_total_applicant_country(), className="card-text")
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
        dbc.Col(html.Button("Download Full Data", id="btn_download_full_applicant_country"), width={'size': 2, 'offset': 0}),
        dbc.Col(html.Button("Download Selected Data", id="btn_download_selected_applicant_country"), width=2),
    ], justify="start", className="mb-0"),
    
    # Data Table
    dash_table.DataTable(
        id='applicant-country-datatable-interactivity',
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
                    id='applicant-country-metric-dropdown',
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
    dbc.Row(dbc.Col(dcc.Graph(id='applicant-country-bar-chart'), width=12)),
    
    # Line Chart
    dbc.Row(dbc.Col(dcc.Graph(id='applicant-country-line-chart'), width=12)),


    # dbc.Row([
    #     dbc.Col(dcc.Link(
    #         html.Div([
    #             html.Img(src='/assets/applicant_country_VOSviewer-screenshot.PNG', style={'max-width': '100%', 'max-height': '600px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}),
    #             # html.P("Inventors")
    #         ]),
    #         target='_blank',  # Opens the link in a new tab
    #         href='http://tinyurl.com/2bv9b594'
    #     ), width={"size": 8, "offset": 1}, className="d-flex justify-content-center mt-5 mb-5"),  
    # ], className="mb-2 d-flex justify-content-center"),
    dbc.Row(
        dbc.Col(
            html.Iframe(
                src="http://tinyurl.com/278vdt5j",
                style={
                    "border": "1px solid #ddd",
                    "width": "100%",  # Adjust width as needed
                    "height": "500px",  # Adjust height as needed
                    "display": "block",
                    "margin-left": "auto",
                    "margin-right": "auto"
                },
                allow="fullscreen",  # This enables fullscreen mode
            ),
            width=12,  # Adjust the column width as needed
        )
    ),
    # Hidden Divs for JSON-serialized data
    html.Div(id='applicant-country-data-storage-full', style={'display': 'none'}),
    html.Div(id='applicant-country-data-storage-selected', style={'display': 'none'}),

    # Hidden element for triggering downloads
    dcc.Download(id="applicant-country-download-dataframe-csv"),
    Footer()  # Include footer at the bottom


], fluid=True)



# Callbacks for the applicant_country page
@callback(
    Output('applicant-country-bar-chart', 'figure'),
    [Input('applicant-country-datatable-interactivity', 'derived_virtual_data'),
     Input('applicant-country-datatable-interactivity', 'derived_virtual_selected_rows'),
     Input('applicant-country-metric-dropdown', 'value')]  # Input from the dropdown
)
def update_applicant_country_bar_chart(rows, derived_virtual_selected_rows, selected_metric):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = pd.DataFrame(rows) if rows is not None else df

    # Check if the selected_metric column exists in the dataframe
    if selected_metric not in dff.columns:
        raise PreventUpdate  # Prevents the callback from firing if selected_metric is not in columns

    if len(derived_virtual_selected_rows) == 0:
        filtered_df = dff.sort_values(selected_metric, ascending=False).head(20)
        title = f'Top 20 Applicant Countries by {selected_metric}'
    else:
        filtered_df = dff.iloc[derived_virtual_selected_rows]
        filtered_df = filtered_df.sort_values(selected_metric, ascending=False)
        title = f'Selected Applicant Countries by {selected_metric}'

    # Plotting the bar chart
    # fig = px.bar(filtered_df, x="Applicant country", y=selected_metric, color="2023 Classification", barmode="group",
    #              category_orders={"Applicant country": filtered_df["Applicant country"].tolist()})  # Ensure consistent ordering
    # fig.update_layout(title=title)
    fig = px.bar(filtered_df, x="Applicant country", y=selected_metric, color="2023 Classification",
             hover_data=[selected_metric, 'First Year', 'Last Year','Mean Patents/Year'],
             barmode="group",
             category_orders={"Applicant country": filtered_df["Applicant country"].tolist()})  # Ensure consistent ordering
             
    fig.update_traces(hovertemplate="Applicant country: %{x}<br>" + selected_metric + ": %{y}<br>First Year: %{customdata[0]}<br>Last Year: %{customdata[1]}<br>Mean Patents/Year: %{customdata[2]}")
    fig.update_layout(title=title)
    return fig


#####


####
@callback(
    Output('applicant-country-line-chart', 'figure'),
    [Input('applicant-country-datatable-interactivity', 'derived_virtual_data'),  # Get the filtered data from the table
     Input('applicant-country-datatable-interactivity', 'derived_virtual_selected_rows'),  # Get the selected rows from the table
     Input('applicant-country-bar-chart', 'clickData')]  # Get the click data from the bar chart
)
def update_applicant_country_line_chart(all_rows_data, slctd_row_indices, clickData):
    # Process the data from the table
    dff = pd.DataFrame(all_rows_data) if all_rows_data is not None else pd.DataFrame()
    selected_applicant_countrys = dff.iloc[slctd_row_indices]['Applicant country'].tolist() if slctd_row_indices else []

    # Process the click data from the bar chart
    if clickData:
        clicked_applicant_country = clickData['points'][0]['x']
        if clicked_applicant_country not in selected_applicant_countrys:
            selected_applicant_countrys.append(clicked_applicant_country)

    # Aggregate data: count patents per year for each applicant_country
    applicant_country_yearly_counts = df_trend.groupby(['Application Year', 'Applicant country']).size().reset_index(name='Patent Count')

    # Create the line chart
    if selected_applicant_countrys:
        filtered_df = applicant_country_yearly_counts[applicant_country_yearly_counts['Applicant country'].isin(selected_applicant_countrys)]
        fig = px.line(filtered_df, x='Application Year', y='Patent Count', color='Applicant country',markers=True)
        fig.update_layout(title='Contribution Trends of Selected applicant_countrys Over Years')
    else:
        # When no applicant_countrys are selected, show the global trend
        df_trend2 = df_trend[['Lens ID','Application Year']].drop_duplicates()
        global_yearly_counts = df_trend2.groupby(['Application Year']).size().reset_index(name='Total Patents')
        fig = px.line(global_yearly_counts, x='Application Year', y='Total Patents',markers=True)
        fig.update_layout(title='Global Trend of Patent Contributions Over Years')
    
    return fig



# ... The rest of the callbacks remain similar to those in inventor_page.py, just change IDs and variables to match the context of applicant_countrys ...

@callback(
    [Output('applicant-country-data-storage-full', 'children'),
     Output('applicant-country-data-storage-selected', 'children')],
    [Input('applicant-country-datatable-interactivity', 'derived_virtual_data'),
     Input('applicant-country-datatable-interactivity', 'derived_virtual_selected_rows')]
)
def store_applicant_country_data(all_rows_data, slctd_row_indices):
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
    Output("applicant-country-download-dataframe-csv", "data"),
    [Input("btn_download_full_applicant_country", "n_clicks"),
     Input("btn_download_selected_applicant_country", "n_clicks"),
     Input('applicant-country-data-storage-full', 'children'),
     Input('applicant-country-data-storage-selected', 'children')],
    prevent_initial_call=True,
)
def download_applicant_country_csv(btn_full, btn_selected, full_data_str, selected_data_str):
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == "btn_download_full_applicant_country":
        df = pd.read_json(full_data_str, orient='split')
        return dcc.send_data_frame(df.to_csv, filename="full_data_applicant_country.csv")
    elif button_id == "btn_download_selected_applicant_country":
        if selected_data_str:
            df = pd.read_json(selected_data_str, orient='split')
            return dcc.send_data_frame(df.to_csv, filename="selected_data_applicant_country.csv")
    return no_update
