# Restaurant Data Collector

Collects restaurant data from Yelp's Fusion API and prepares it for loading into PostgreSQL.

# Data Collection Strategy

The collector fetches restaurant data using three different sorting methods to ensure variety:
- `rating`: Highly-rated restaurants
- `review_count`: Popular establishments
- `best_match`: Yelp's default algorithm

For each location and cuisine combination, it collects:
- 10 restaurants from each sort method
- Across 10 different cuisines
- For specified locations (e.g., "New York, NY", "Los Angeles, CA")

This approach provides:
- Natural variation in ratings and popularity
- Mix of established and newer restaurants
- Coverage across different price points
- Approximately 300 restaurants per location

## Usage

Run the collector:
```bash
poetry shell
python collector/yelp_collector.py
```
Output files are saved to `raw_data/` in JSON format:
- `restaurants_<location>_<timestamp>.json`