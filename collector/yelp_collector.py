import os
from dotenv import load_dotenv
from pathlib import Path
import requests
import json
from datetime import datetime
import time

load_dotenv()

class YelpCollector:
    LOCATIONS = [
        #'New York, NY',
        #'Brooklyn, NY'
        #'Los Angeles, CA'
    ]
    
    CUISINES = [
        'Japanese',
        'Italian',
        'Chinese',
        'Thai',
        'Mexican',
        'Korean',
        'Mediterranean',
        'Indian',
        'Vietnamese',
        'American'
    ]
    
    SORT_TYPES = [
        'rating',     # Get some highly-rated spots
        'review_count',  # Get some popular spots
        'best_match'    # Get Yelp's default mix
    ]

    def __init__(self):
        self.api_key = os.getenv('YELP_API_KEY')
        if not self.api_key:
            raise ValueError("YELP_API_KEY not found in environment variables")
            
        self.endpoint = 'https://api.yelp.com/v3/businesses/search'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

        # Create raw_data directory if it doesn't exist
        self.data_dir = Path(__file__).parent.parent / 'raw_data'
        self.data_dir.mkdir(exist_ok=True)

    def collect_location(self, location):
        """Collect restaurants for all cuisines in a location"""
        location_data = []
        
        for cuisine in self.CUISINES:
            print(f"Collecting {cuisine} restaurants in {location}...")
            results = self.get_restaurants(cuisine=cuisine, location=location)
            if results:
                location_data.extend(results)
            time.sleep(1)  # Be nice to the API
        
        # Save data for this location
        filename = self.data_dir / f'restaurants_{location.split(",")[0].lower().replace(" ", "_")}_{datetime.now().strftime("%Y%m%d")}.json'
        self.save_results(location_data, filename)
        print(f"Saved {len(location_data)} restaurants for {location}")
        
        return location_data

    def get_restaurants(self, cuisine, location):
        all_restaurants = []
        
        for sort_by in self.SORT_TYPES:
            params = {
                'term': cuisine,
                'location': location,
                'limit': 10,  # 10 from each sort type
                'sort_by': sort_by
            }

            response = requests.get(
                self.endpoint,
                headers=self.headers,
                params=params
            )

            if response.status_code == 200:
                data = response.json()
                print(f"Found {len(data['businesses'])} {cuisine} restaurants ({sort_by})")
                
                for business in data['businesses']:
                    all_restaurants.append({
                        'name': business['name'],
                        'categories': [cat['title'] for cat in business['categories']],
                        'cuisine_searched': cuisine,
                        'rating': business['rating'],
                        'review_count': business['review_count'],
                        'price': business.get('price', 'N/A'),
                        'address': {
                            'street': business['location']['address1'],
                            'city': business['location']['city'],
                            'zip': business['location']['zip_code'],
                            'state': business['location']['state'],
                            'borough': location.split(',')[0]
                        },
                        'sort_method': sort_by  # Track how we found this restaurant
                    })
            else:
                print(f"Error: {response.status_code}")
                continue
                
            time.sleep(0.5)  # Small delay between sort types
            
        return all_restaurants

    def save_results(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)


if __name__ == '__main__':
    collector = YelpCollector()
    
    # Collect for each location
    for location in collector.LOCATIONS:
        print(f"\nCollecting data for {location}...")
        collector.collect_location(location)