import os
import json


config = json.load(open('config.json'))

# Configuration file for the CRM application
# This file contains the database configuration and other settings
USERNAME = config.get('username')
PASSWORD = config.get('password')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, config.get('database'))
