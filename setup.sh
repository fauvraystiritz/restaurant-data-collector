#!/bin/bash

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Configure Poetry to not create its own virtual environment
poetry config virtualenvs.create false --local

# Install dependencies using Poetry
poetry install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "YELP_API_KEY=your_api_key_here
DB_NAME=your_db_name
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost" > .env
    echo "Created .env file - please update with your actual credentials"
fi

echo "Setup complete! Don't forget to run 'source venv/bin/activate' to activate the virtual environment"