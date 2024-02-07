# main_page.py
from components import Navbar, Footer
import dash_bootstrap_components as dbc
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load your data (Make sure the path is correct)
df_appl_trend = pd.read_csv('./data/applicant_year_table.csv')
# Load inventor data
df_inv_trend = pd.read_csv('./data/inventor_year_table.csv')
# Load inventor data
df_full_data = pd.read_csv('./data/full_data_table.csv')

# Aggregate patent count per year
df_appl_trend2 = df_appl_trend[['Lens ID','Application Year']].drop_duplicates()
global_yearly_counts = df_appl_trend2.groupby(['Application Year']).size().reset_index(name='Total Patents')
fig_patents_over_time = px.line(global_yearly_counts, x='Application Year', y='Total Patents',markers=True  # Add markers for each data point
)
fig_patents_over_time.update_layout(title='Global Trend of Patent Contributions Over Years')

##
df_country_trend = pd.read_csv('./data/applicant_country_year_table.csv')

# Ensure 'Application Year' is of type int for proper sorting and comparison
df_country_trend['Application Year'] = df_country_trend['Application Year'].astype(int)

# Calculate the total patents per country per year
df_total_patents = df_country_trend.groupby(['Application Year', 'Applicant country', 'iso_alpha', 'Region']).size().reset_index(name='Total Patents')

# Create a complete DataFrame of all combinations of 'Application Year' and 'Applicant country'
all_years = df_country_trend['Application Year'].unique()
all_countries = df_country_trend['Applicant country'].unique()
df_full = pd.MultiIndex.from_product([all_years, all_countries], names=['Application Year', 'Applicant country']).to_frame(index=False)

# Merge the complete DataFrame with the total patents data
df_full = df_full.merge(df_total_patents, on=['Application Year', 'Applicant country'], how='left')

# Sort the result by 'Application Year' and 'Applicant country'
df_full = df_full.sort_values(by=['Applicant country', 'Application Year'])
df_full['Total Patents'] = df_full['Total Patents'].fillna(0)

# Calculate cumulative patents per country per year, forward filling the missing values
df_full['Cumulative Patents'] = df_full.groupby(['Applicant country'])['Total Patents'].cumsum().fillna(method='ffill')

# Fill NaN in 'iso_alpha', 'Region', and 'Cumulative Patents' after merging
df_full['iso_alpha'] = df_full.groupby('Applicant country')['iso_alpha'].ffill().bfill()
df_full['Region'] = df_full.groupby('Applicant country')['Region'].ffill().bfill()
df_full['Cumulative Patents'] = df_full['Cumulative Patents'].fillna(0)  # Fill NaN values with 0

# Get the latest year for the default display
latest_year = df_full['Application Year'].max()

fig_appl_country_trend = px.scatter_geo(df_full,
                    locations="iso_alpha",
                    color="Region",
                    hover_name="Applicant country",
                    animation_frame="Application Year",
                    size="Cumulative Patents",  # Ensure no NaN values here
                    projection="natural earth")

# Update layout to show the latest year by default
fig_appl_country_trend.update_layout(
    title_text='Evolution of Cumulative Patent Counts per Country per Year',
    geo=dict(
        showcoastlines=True,
    ),
    updatemenus=[dict(
        buttons=[dict(
            args=[None, {"frame": {"duration": 500, "redraw": True},
                         "fromcurrent": True, "transition": {"duration": 300, "easing": "quadratic-in-out"}}],
            label="Play",
            method="animate"
        ),
            dict(
                args=[[f"{latest_year}"], {"frame": {"duration": 0, "redraw": True},
                                           "mode": "immediate",
                                           "transition": {"duration": 0}}],
                label="Reset to Latest Year",
                method="animate"
            )]
    )],
    # Specify the figure size here
    width=1000,  # Width in pixels
    height=700,   # Height in pixels
)

##################################################""""""
import plotly.express as px
import pandas as pd

df_jurisdiction_trend = pd.read_csv('./data/jurisdiction_year_table.csv')

# Ensure 'Application Year' is of type int for proper sorting and comparison
df_jurisdiction_trend['Application Year'] = df_jurisdiction_trend['Application Year'].astype(int)

# Calculate the total patents per jurisdiction per year
df_total_patents = df_jurisdiction_trend.groupby(['Application Year', 'Jurisdiction', 'iso_alpha', 'Region']).size().reset_index(name='Total Patents')

# Create a complete DataFrame of all combinations of 'Application Year' and 'Jurisdiction'
all_years = df_jurisdiction_trend['Application Year'].unique()
all_jurisdictions = df_jurisdiction_trend['Jurisdiction'].unique()
df_full = pd.MultiIndex.from_product([all_years, all_jurisdictions], names=['Application Year', 'Jurisdiction']).to_frame(index=False)

# Merge the complete DataFrame with the total patents data
df_full = df_full.merge(df_total_patents, on=['Application Year', 'Jurisdiction'], how='left')

# Sort the result by 'Application Year' and 'Jurisdiction'
df_full = df_full.sort_values(by=['Jurisdiction', 'Application Year'])
df_full['Total Patents'] = df_full['Total Patents'].fillna(0)

# Calculate cumulative patents per jurisdiction per year, forward filling the missing values
df_full['Cumulative Patents'] = df_full.groupby(['Jurisdiction'])['Total Patents'].cumsum().fillna(method='ffill')

# Fill NaN in 'iso_alpha', 'Region', and 'Cumulative Patents' after merging
df_full['iso_alpha'] = df_full.groupby('Jurisdiction')['iso_alpha'].ffill().bfill()
df_full['Region'] = df_full.groupby('Jurisdiction')['Region'].ffill().bfill()
df_full['Cumulative Patents'] = df_full['Cumulative Patents'].fillna(0)  # Fill NaN values with 0

# Get the latest year for the default display
latest_year = df_full['Application Year'].max()

fig_juris_trend = px.scatter_geo(df_full,
                    locations="iso_alpha",
                    color="Region",
                    hover_name="Jurisdiction",
                    animation_frame="Application Year",
                    size="Cumulative Patents",  # Ensure no NaN values here
                    projection="natural earth")

# Update layout to show the latest year by default
fig_juris_trend.update_layout(
    title_text='Evolution of Cumulative Patent Counts per Jurisdiction per Year',
    geo=dict(
        showcoastlines=True,
    ),
    updatemenus=[dict(
        buttons=[dict(
            args=[None, {"frame": {"duration": 500, "redraw": True},
                         "fromcurrent": True, "transition": {"duration": 300, "easing": "quadratic-in-out"}}],
            label="Play",
            method="animate"
        ),
            dict(
                args=[[f"{latest_year}"], {"frame": {"duration": 0, "redraw": True},
                                           "mode": "immediate",
                                           "transition": {"duration": 0}}],
                label="Reset to Latest Year",
                method="animate"
            )]
            
    )],
    # Specify the figure size here
    width=1000,  # Width in pixels
    height=700,   # Height in pixels
    # className="mb-4 d-flex justify-content-center",
)

##############################33
# Define callback functions for dynamic content updates (placeholders for now)
def update_total_patents():
    # Placeholder function to update total patents dynamically
    return str(df_full_data['Lens ID'].nunique())

def update_top_inventor():
    # Placeholder function to update top inventor dynamically
    return df_inv_trend['Inventor'].mode()[0]  # Example: mode to get the most common inventor

def update_top_applicant():
    # Placeholder function to update top applicant dynamically
    return df_appl_trend['Applicant'].mode()[0]

def update_top_applicant_country():
    # Placeholder function to update top applicant country dynamically
    return df_country_trend['Applicant country'].mode()[0]

def update_most_active_jurisdiction():
    # Placeholder function to update the most active jurisdiction dynamically
    return df_jurisdiction_trend['Jurisdiction'].mode()[0]

def update_average_citations():
    # Placeholder function to update average citations dynamically
    return str(round(df_full_data['Cited by Patent Count'].mean(), 2))

####################
# navbar = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("Home", href="/")),
#         dbc.NavItem(dbc.NavLink("Inventors", href="/inventor")),
#         dbc.NavItem(dbc.NavLink("Applicants", href="/applicants")),
#         dbc.NavItem(dbc.NavLink("Applicants countries", href="/applicants_countries")),
#         dbc.NavItem(dbc.NavLink("Jurisdictions", href="/jurisdiction")),

#         # ... other links ...
#     ],
#     brand="Immune Checkpoint Therapy Patent Analysis",
#     brand_href="/",
#     color="primary",
#     dark=True,
# )


##############################################################""""
layout = dbc.Container([
    Navbar(),  # Include navbar at the top
    # navbar,
    dbc.Row(dbc.Col(html.H1("Immune Checkpoint Therapy Patent Analysis"), className="text-center mt-5 mb-4")),
    
    dbc.Row(dbc.Col(html.P(
        "Explore comprehensive analytics on immune checkpoint therapy patents. Navigate through different sections for detailed insights on Inventors, Applicants, Applicant Countries, and Jurisdictions."),
        width={'size': 8, 'offset': 2}, className="text-center mb-3"
    )),
    
    # dbc.Row([
    #     dbc.Col(dcc.Link('Inventors', href='/inventor'), width={"size": 2, "offset": 1}),
    #     dbc.Col(dcc.Link('Applicants', href='/applicants'), width={"size": 2}),
    #     dbc.Col(dcc.Link('Applicant countries', href='/applicants_countries'), width={"size": 2}),
    #     dbc.Col(dcc.Link('Jurisdictions', href='/jurisdiction'), width={"size": 2}),
    # ], className="mb-4 d-flex justify-content-center"),
    

    # ... other components ...

    dbc.Row([
        dbc.Col(dcc.Link(
            html.Div([
                html.Img(src='/assets/inventors_icon.jpg', style={'width': '100px', 'height': '100px'}),
                html.P("Inventors")
            ]),
            href='/inventor'
        ), width={"size": 2, "offset": 1}, className="text-center"),
        dbc.Col(dcc.Link(
            html.Div([
                html.Img(src='/assets/applicants_icon.jpg', style={'width': '100px', 'height': '100px'}),
                html.P("Applicants")
            ]),
            href='/applicants'
        ), width={"size": 2}, className="text-center"),
        dbc.Col(dcc.Link(
            html.Div([
                html.Img(src='/assets/applicant_countries_icon.jpg', style={'width': '100px', 'height': '100px'}),
                html.P("Applicant Countries")
            ]),
            href='/applicants_countries'
        ), width={"size": 2}, className="text-center"),
        dbc.Col(dcc.Link(
            html.Div([
                html.Img(src='/assets/jurisdictions_icon.jpg', style={'width': '100px', 'height': '100px'}),
                html.P("Jurisdictions")
            ]),
            href='/jurisdiction'
        ), width={"size": 2}, className="text-center"),
    ], className="mb-3 d-flex justify-content-center"),

    # ... other components ...



    # High-Level Summary or Key Metrics
    
    # First row of metrics
    dbc.Row([
        dbc.Col(html.Div([
            html.H3("Total Patents", className="text-center"),
            html.P(update_total_patents(), id="total-patents", className="lead text-center")
        ]), width=4, className="d-flex justify-content-center"),  # Add flexbox classes
        dbc.Col(html.Div([
            html.H3("Top Inventor", className="text-center"),
            html.P(update_top_inventor(), id="top-inventor", className="lead text-center")
        ]), width=4, className="d-flex justify-content-center"),
        dbc.Col(html.Div([
            html.H3("Top Applicant", className="text-center"),
            html.P(update_top_applicant(), id="top-applicant", className="lead text-center")
        ]), width=4, className="d-flex justify-content-center"),
    ], className="mb-2 d-flex justify-content-center"),  # Center the columns in the row
    
    # Second row of metrics
    dbc.Row([
        dbc.Col(html.Div([
            html.H3("Top Applicant Country", className="text-center"),
            html.P(update_top_applicant_country(), id="top-applicant-country", className="lead text-center")
        ]), width=4, className="d-flex justify-content-center"),
        dbc.Col(html.Div([
            html.H3("Most Active Jurisdiction", className="text-center"),
            html.P(update_most_active_jurisdiction(), id="active-jurisdiction", className="lead text-center")
        ]), width=4, className="d-flex justify-content-center"),
        dbc.Col(html.Div([
            html.H3("Average Citations", className="text-center"),
            html.P(update_average_citations(), id="avg-citations", className="lead text-center")
        ]), width=4, className="d-flex justify-content-center"),
    ], className="mb-2 d-flex justify-content-center"),
    
    # ... other components ...


    # Visualizations
    # ... your code for visualizations ...
        # Section for the line chart
    dbc.Row(dbc.Col(dcc.Graph(
        id='patents-over-time-graph',
        figure=fig_patents_over_time  # This is the line chart you created
    ), width=12)),

    dbc.Row(dbc.Col(dcc.Graph(
        id='patents-over-time-graph-appl-country',
        figure=fig_appl_country_trend  # This is the line chart you created
    ), width=12), className="mb-2 d-flex justify-content-center"),
    

    dbc.Row([dbc.Col(dcc.Graph(
        id='patents-over-time-graph-jurisdiction',
        figure=fig_juris_trend  # This is the line chart you created
    ), width=12)], className="mb-2 d-flex justify-content-center"),
    
    # Example Row with an image link
    # dbc.Row(
    #     dbc.Col(
    #         html.A(
    #             html.Img(src='/assets/inventor_icon.jpg', style={'width': '100%', 'height': 'auto'}),
    #             href='https://www.example.com',  # Link URL
    #             target='_blank'  # Opens the link in a new tab
    #         ),
    #         width={"size": 6, "offset": 3}, className="d-flex justify-content-center mb-4"
    #     )
    # ),

    # dbc.Row(
    #     dbc.Col(
    #         html.Iframe(
    #             src="http://tinyurl.com/278vdt5j",
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

    # User Guide or Instructions
    dbc.Row(dbc.Col(html.P("Navigate through the tabs to explore detailed analytics on each category. Use the interactive charts and tables for in-depth analysis."), className="text-center")),
    
    # Footer
    dbc.Row(dbc.Col(html.Small("Data Source: Lens.org | Last Updated: 28/01/2024 | By Maxime Descartes Mbogning"), className="text-center")),
], fluid=True)

