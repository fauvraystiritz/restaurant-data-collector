import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

# Load environment variables
load_dotenv()

class YelpCollector:
    def __init__(self):
        self.api_key = os.getenv('YELP_API_KEY')
        if not self.api_key:
            raise ValueError("YELP_API_KEY not found in environment variables")
            
        self.endpoint = 'https://api.yelp.com/v3/businesses/search'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

    def get_restaurants(self, cuisine='ramen', location='East Village, New York, NY'):
        params = {
            'term': cuisine,
            'location': location,
            'limit': 50,
            'sort_by': 'rating'
        }

        response = requests.get(
            self.endpoint,
            headers=self.headers,
            params=params
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def save_results(self, data, filename=None):
        if filename is None:
            filename = f'restaurants_{datetime.now().strftime("%Y%m%d")}.json'
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)


if __name__ == '__main__':
    # This will run if we execute yelp_api.py directly
    collector = YelpCollector()
    results = collector.get_restaurants()
    if results:
        collector.save_results(results)
        print("Data collected and saved!")