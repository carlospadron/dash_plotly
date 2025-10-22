import sqlite3
import pandas as pd


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
