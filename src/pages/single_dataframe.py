import pandas as pd
from dash import html, dcc, dash_table, register_page, callback, Input, Output
import plotly.express as px
from src.lib import read_data_from_db

# Register this page with Dash
register_page(__name__, path='/', name='Single DataFrame')


def create_dashboard_content(df):
    """Create the dashboard content from a dataframe"""
    return [
        # Statistics section
        html.Div([
            html.H4("Database Statistics"),
            html.P(f"Total Records: {len(df)}"),
            html.P(f"Total Sales: ${df['sales'].sum():,.2f}"),
            html.P(f"Average Sales: ${df['sales'].mean():,.2f}"),
        ], style={'margin': '20px'}),
        
        # Charts section
        html.Div([
            html.Div([
                html.H4("Sales by Product"),
                dcc.Graph(
                    id='sales-by-product',
                    figure=px.bar(
                        df.groupby('product')['sales'].sum().reset_index(),
                        x='product',
                        y='sales',
                        title='Total Sales by Product',
                        color='sales',
                        color_continuous_scale='Viridis'
                    )
                )
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            html.Div([
                html.H4("Sales by Region"),
                dcc.Graph(
                    id='sales-by-region',
                    figure=px.pie(
                        df.groupby('region')['sales'].sum().reset_index(),
                        values='sales',
                        names='region',
                        title='Sales Distribution by Region'
                    )
                )
            ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ], style={'margin': '20px'}),
        
        # Data table section
        html.Div([
            html.H4("Data Table"),
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                page_size=10,
                export_format='xlsx',
                export_headers='display',
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px'
                },
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ]
            )
        ], style={'margin': '20px'})
    ]


# Define the layout for this page
def layout():
    # Read data from database
    df = read_data_from_db()
    
    return html.Div([
        html.Div([
            html.H1("Sales Dashboard - Single DataFrame", 
                    style={'textAlign': 'center', 'margin': '20px', 'display': 'inline-block', 'width': '80%'}),
            html.Button('🔄 Refresh Data', id='refresh-button', n_clicks=0, style={
                'backgroundColor': '#3498db',
                'color': 'white',
                'padding': '10px 20px',
                'fontSize': '14px',
                'border': 'none',
                'borderRadius': '5px',
                'cursor': 'pointer',
                'margin': '20px',
                'float': 'right'
            }),
        ], style={'width': '100%', 'overflow': 'auto'}),
        
        html.Hr(),
        
        # Container for dynamic content
        html.Div(id='dashboard-content', children=create_dashboard_content(df))
    ])


@callback(
    Output('dashboard-content', 'children'),
    Input('refresh-button', 'n_clicks'),
    prevent_initial_call=True
)
def refresh_data(n_clicks):
    """Refresh data from database when button is clicked"""
    df = read_data_from_db()
    return create_dashboard_content(df)
