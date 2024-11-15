#!/bin/bash

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install initial dependencies
pip install scrapy

# Create requirements.txt
pip freeze > requirements.txt

# Initialize scrapy project
scrapy startproject collector .

echo "Setup complete! Don't forget to run 'source venv/bin/activate' to activate the virtual environment"