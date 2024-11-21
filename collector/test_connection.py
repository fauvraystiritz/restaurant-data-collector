import os
from dotenv import load_dotenv
import psycopg2
from pathlib import Path

# Get the project root directory (one level up from collector)
project_root = Path(__file__).parent.parent

def test_db_connection():
    # Load environment variables from project root
    load_dotenv(project_root / '.env')
    
    # Print connection details for debugging
    print("Attempting to connect with:")
    print(f"User: {os.getenv('DB_USER')}")
    print(f"Database: {os.getenv('DB_NAME')}")
    print(f"Host: {os.getenv('DB_HOST')}")
    print(f"Port: 5432")
    
    try:
        # Attempt connection
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port='5432'
        )
        print("\nConnection successful!")
        
        # Test a simple query
        cur = conn.cursor()
        cur.execute('SELECT current_user, current_database();')
        user, db = cur.fetchone()
        print(f"\nConnected as: {user}")
        print(f"Database: {db}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"\nConnection failed with error:\n{str(e)}")

if __name__ == "__main__":
    test_db_connection()