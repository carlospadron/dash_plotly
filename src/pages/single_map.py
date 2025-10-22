import pandas as pd
import json
from dash import html, dcc, dash_table, register_page, callback, Input, Output, callback_context
import plotly.graph_objects as go
from src.lib import read_geo_data_from_db

# Register this page with Dash
register_page(__name__, path='/map', name='Single Map')


def create_map_figure(df, selected_ids=None):
    """Create a Plotly map with GeoJSON polygons"""
    fig = go.Figure()
    
    # Add each polygon to the map
    for idx, row in df.iterrows():
        geojson = json.loads(row['geojson'])
        coords = geojson['coordinates'][0]
        
        # Extract lat/lon for the polygon
        lons = [coord[0] for coord in coords]
        lats = [coord[1] for coord in coords]
        
        # Determine if this polygon is selected
        is_selected = selected_ids and row['id'] in selected_ids
        
        fig.add_trace(go.Scattermapbox(
            lon=lons,
            lat=lats,
            mode='lines',
            fill='toself',
            fillcolor='rgba(255, 0, 0, 0.3)' if is_selected else 'rgba(0, 123, 255, 0.3)',
            line=dict(width=2, color='red' if is_selected else 'blue'),
            name=row['name'],
            text=f"{row['name']}<br>Population: {row['population']:,}<br>Area: {row['area_km2']} km²",
            hoverinfo='text',
            customdata=[row['id']]
        ))
    
    # Update map layout
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',
            center=dict(lat=40.72, lon=-74.01),
            zoom=11
        ),
        showlegend=True,
        height=600,
        margin=dict(l=0, r=0, t=0, b=0),
        clickmode='event+select',
        uirevision='constant',  # Preserve zoom/pan state
        hovermode='closest'
    )
    
    return fig


def layout(**kwargs):
    # Read data from database
    df = read_geo_data_from_db()
    
    return html.Div([
        html.H1("Geospatial Data Viewer", style={'textAlign': 'center', 'margin': '20px'}),
        html.Hr(),
        
        html.Div([
            html.P("Click on polygons in the map or select rows in the table to highlight them. Selections are synchronized.",
                   style={'fontSize': '14px', 'color': '#666', 'textAlign': 'center'})
        ], style={'margin': '20px'}),
        
        # Map section
        html.Div([
            html.H4("Map View"),
            dcc.Graph(
                id='geo-map',
                figure=create_map_figure(df),
                config={
                    'scrollZoom': True,  # Enable scroll to zoom
                    'displayModeBar': False,  # Hide the toolbar
                    'doubleClick': 'reset'  # Double-click to reset view
                }
            )
        ], style={'margin': '20px'}),
        
        # Table section
        html.Div([
            html.H4("Data Table"),
            dash_table.DataTable(
                id='geo-table',
                columns=[
                    {"name": "ID", "id": "id"},
                    {"name": "Name", "id": "name"},
                    {"name": "Population", "id": "population"},
                    {"name": "Area (km²)", "id": "area_km2"}
                ],
                data=df[['id', 'name', 'population', 'area_km2']].to_dict('records'),
                row_selectable='multi',
                selected_rows=[],
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px'
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
                    },
                    {
                        'if': {'state': 'selected'},
                        'backgroundColor': 'rgba(255, 0, 0, 0.2)',
                        'border': '1px solid red'
                    }
                ]
            )
        ], style={'margin': '20px'})
    ])


@callback(
    Output('geo-map', 'figure'),
    Input('geo-table', 'selected_rows'),
    prevent_initial_call=True
)
def update_map_from_table(selected_rows):
    """Update map highlighting based on table selection"""
    df = read_geo_data_from_db()
    
    if selected_rows:
        selected_ids = [df.iloc[i]['id'] for i in selected_rows]
    else:
        selected_ids = None
    
    return create_map_figure(df, selected_ids)


@callback(
    Output('geo-table', 'selected_rows'),
    Input('geo-map', 'clickData'),
    Input('geo-table', 'selected_rows'),
    prevent_initial_call=True
)
def update_table_from_map(clickData, current_selection):
    """Update table selection based on map clicks - toggle selection"""
    # Check which input triggered the callback
    if not callback_context.triggered:
        return current_selection or []
    
    trigger = callback_context.triggered[0]['prop_id']
    
    # Only process if the map was clicked
    if 'geo-map' in trigger and clickData and 'points' in clickData:
        # Get the clicked polygon's curve number (trace index)
        curve_number = clickData['points'][0]['curveNumber']
        
        # Initialize selection if None
        if current_selection is None:
            current_selection = []
        
        # Toggle selection: remove if already selected, add if not
        if curve_number in current_selection:
            current_selection.remove(curve_number)
        else:
            current_selection.append(curve_number)
        
        return current_selection
    
    return current_selection or []
