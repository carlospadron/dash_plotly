from dash import Dash, html, dcc, page_container
from lib import create_sample_database


def main():
    # Create sample database
    create_sample_database()
    
    # Initialize the Dash app with multi-page support
    app = Dash(__name__, use_pages=True)
    
    # Create the app layout with navigation
    app.layout = html.Div([
        html.Div([
            html.H1("Sales Analytics Dashboard", style={
                'textAlign': 'center',
                'margin': '20px',
                'color': '#2c3e50'
            }),
            
            # Navigation bar
            html.Div([
                dcc.Link('Single DataFrame', href='/', style={
                    'padding': '10px 20px',
                    'margin': '0 10px',
                    'textDecoration': 'none',
                    'backgroundColor': '#3498db',
                    'color': 'white',
                    'borderRadius': '5px',
                    'display': 'inline-block'
                }),
                # Add more page links here as you create them
            ], style={
                'textAlign': 'center',
                'margin': '20px',
                'padding': '10px',
                'backgroundColor': '#ecf0f1',
                'borderRadius': '5px'
            }),
            
            html.Hr(),
        ]),
        
        # Page content will be rendered here
        page_container
    ])
    
    # Run the app
    print("Starting Dash multi-page app...")
    print("Open your browser and navigate to: http://127.0.0.1:8050")
    app.run(debug=True)


if __name__ == "__main__":
    main()
