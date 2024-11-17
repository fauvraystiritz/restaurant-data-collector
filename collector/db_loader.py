import json
import psycopg2
from psycopg2.extras import execute_values
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

def load_restaurants():
    # Database connection
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST', 'localhost')
    )
    cur = conn.cursor()

    # Find all restaurant JSON files
    data_files = Path('.').glob('restaurants_*.json')
    
    for file_path in data_files:
        print(f"Processing {file_path}...")
        with open(file_path) as f:
            restaurants = json.load(f)
            
        # Prepare data for insertion
        values = [
            (
                restaurant['name'],
                restaurant['cuisine_searched'],
                restaurant['rating'],
                restaurant['review_count'],
                restaurant['price'] if restaurant['price'] != 'N/A' else None,
                json.dumps(restaurant['categories']),  # Convert list to JSON
                json.dumps(restaurant['address']),     # Convert dict to JSON
                restaurant['sort_method'],
                restaurant['address']['borough']
            )
            for restaurant in restaurants
        ]
        
        # Bulk insert
        execute_values(
            cur,
            """
            INSERT INTO restaurants 
                (name, cuisine_searched, rating, review_count, price, 
                 categories, address, sort_method, borough)
            VALUES %s
            """,
            values
        )
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    load_restaurants()