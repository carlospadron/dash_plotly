import pandas as pd
from dash import html, dash_table, register_page, callback, Input, Output, State
from src.lib import read_data_from_db, save_data_to_db

# Register this page with Dash
register_page(__name__, path='/editor', name='Single Editor')


# Define the layout for this page
def layout():
    # Read data from database
    df = read_data_from_db()
    
    return html.Div([
        html.H1("Data Editor", style={'textAlign': 'center', 'margin': '20px'}),
        html.Hr(),
        
        # Instructions
        html.Div([
            html.H4("Edit Your Data"),
            html.P("Click on any cell to edit its value. Delete rows using the X button. Click 'Save to Database' when done.", 
                   style={'fontSize': '14px', 'color': '#666'}),
        ], style={'margin': '20px'}),
        
        # Data table section
        html.Div([
            dash_table.DataTable(
                id='editable-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                page_size=15,
                editable=True,
                row_deletable=True,
                export_format='xlsx',
                export_headers='display',
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'minWidth': '100px'
                },
                style_header={
                    'backgroundColor': 'rgb(52, 152, 219)',
                    'color': 'white',
                    'fontWeight': 'bold'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ]
            ),
            
            # Save button and status message
            html.Div([
                html.Button('Save to Database', id='save-button', n_clicks=0, style={
                    'backgroundColor': '#27ae60',
                    'color': 'white',
                    'padding': '10px 30px',
                    'fontSize': '16px',
                    'border': 'none',
                    'borderRadius': '5px',
                    'cursor': 'pointer',
                    'marginTop': '20px',
                    'marginRight': '10px'
                }),
                html.Div(id='save-status', style={
                    'display': 'inline-block',
                    'marginLeft': '20px',
                    'fontSize': '16px',
                    'fontWeight': 'bold'
                })
            ])
        ], style={'margin': '20px'})
    ])


@callback(
    Output('save-status', 'children'),
    Output('save-status', 'style'),
    Input('save-button', 'n_clicks'),
    State('editable-table', 'data'),
    prevent_initial_call=True
)
def save_changes(n_clicks, table_data):
    """Save the edited table data to the database"""
    if n_clicks > 0:
        try:
            # Convert table data to DataFrame
            df = pd.DataFrame(table_data)
            
            # Save to database
            save_data_to_db(df)
            
            return "✓ Changes saved successfully!", {
                'display': 'inline-block',
                'marginLeft': '20px',
                'fontSize': '16px',
                'fontWeight': 'bold',
                'color': '#27ae60'
            }
        except Exception as e:
            return f"✗ Error saving: {str(e)}", {
                'display': 'inline-block',
                'marginLeft': '20px',
                'fontSize': '16px',
                'fontWeight': 'bold',
                'color': '#e74c3c'
            }
    
    return "", {'display': 'none'}
