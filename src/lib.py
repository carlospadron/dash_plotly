import sqlite3
import pandas as pd
import geopandas as gpd
import json


def create_sample_database():
    """Create a sample SQLite database with sample data"""
    conn = sqlite3.connect('sample_data.db')
    
    # Create sample data
    data = {
        'id': range(1, 21),
        'product': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'] * 4,
        'sales': [250, 380, 420, 190, 560, 310, 450, 280, 520, 390, 
                  470, 330, 410, 290, 580, 350, 440, 310, 490, 420],
        'region': ['North', 'South', 'East', 'West', 'North'] * 4,
        'quarter': ['Q1'] * 5 + ['Q2'] * 5 + ['Q3'] * 5 + ['Q4'] * 5
    }
    
    df = pd.DataFrame(data)
    df.to_sql('sales_data', conn, if_exists='replace', index=False)
    conn.close()
    print("Sample database created successfully!")


def read_data_from_db():
    """Read data from SQLite database"""
    conn = sqlite3.connect('sample_data.db')
    query = "SELECT * FROM sales_data"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_column_types():
    """Get the data types of columns from the database"""
    df = read_data_from_db()
    return df.dtypes.to_dict()


def save_data_to_db(df):
    """Save dataframe to SQLite database preserving original data types"""
    # Get original column types
    original_types = get_column_types()
    
    # Convert columns back to their original types
    df = df.copy()  # Don't modify the original
    for col, dtype in original_types.items():
        if col in df.columns:
            try:
                if pd.api.types.is_numeric_dtype(dtype):
                    # Convert to numeric, handling errors
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    # Preserve integer vs float
                    if pd.api.types.is_integer_dtype(dtype):
                        df[col] = df[col].astype('Int64')  # Nullable integer
                else:
                    # Keep as string/object
                    df[col] = df[col].astype(str)
            except Exception as e:
                print(f"Warning: Could not convert column {col}: {e}")
    
    conn = sqlite3.connect('sample_data.db')
    df.to_sql('sales_data', conn, if_exists='replace', index=False)
    conn.close()
    print("Data saved to database successfully!")


def create_sample_geo_database():
    """Create a sample geospatial database with polygon data"""
    conn = sqlite3.connect('sample_data.db')
    
    # Create sample GeoJSON polygons (simplified city boundaries)
    geo_data = {
        'id': [1, 2, 3, 4, 5],
        'name': ['Downtown', 'Riverside', 'Hillside', 'Lakefront', 'Industrial'],
        'population': [45000, 32000, 28000, 51000, 15000],
        'area_km2': [12.5, 18.3, 22.1, 15.7, 25.4],
        'geojson': [
            json.dumps({"type": "Polygon", "coordinates": [[[-74.01, 40.71], [-74.00, 40.71], [-74.00, 40.72], [-74.01, 40.72], [-74.01, 40.71]]]}),
            json.dumps({"type": "Polygon", "coordinates": [[[-74.02, 40.71], [-74.01, 40.71], [-74.01, 40.72], [-74.02, 40.72], [-74.02, 40.71]]]}),
            json.dumps({"type": "Polygon", "coordinates": [[[-74.00, 40.72], [-73.99, 40.72], [-73.99, 40.73], [-74.00, 40.73], [-74.00, 40.72]]]}),
            json.dumps({"type": "Polygon", "coordinates": [[[-74.01, 40.72], [-74.00, 40.72], [-74.00, 40.73], [-74.01, 40.73], [-74.01, 40.72]]]}),
            json.dumps({"type": "Polygon", "coordinates": [[[-74.02, 40.72], [-74.01, 40.72], [-74.01, 40.73], [-74.02, 40.73], [-74.02, 40.72]]]}),
        ]
    }
    
    df = pd.DataFrame(geo_data)
    df.to_sql('geo_data', conn, if_exists='replace', index=False)
    conn.close()
    print("Sample geo database created successfully!")


def read_geo_data_from_db():
    """Read geospatial data from SQLite database"""
    conn = sqlite3.connect('sample_data.db')
    query = "SELECT * FROM geo_data"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

