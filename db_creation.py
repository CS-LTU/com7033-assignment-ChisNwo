# setup file for databases
# information about databases and their use in app.py

import sqlite3
from pymongo import MongoClient
import os


def setup_sqlite():
    # Set up SQLite database for user accounts
    conn = sqlite3.connect('user_base.db')
    cursor = conn.cursor()

    # Create users table with fields
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()


def setup_mongodb():
    # Set up MongoDB for patient medical information
    client = MongoClient('mongodb://localhost:27017/')
    db = client['stroke_management']

    # Create collection if it doesn't exist
    if 'patients_list' not in db.list_collection_names():
        db.create_collection('patients_list')

    # Create or get the patients collection
    if 'patients-list' not in db.list_collection_names():
        db.create_collection('patients_list')

    # Set rules for patient data
    db.command({
        'collMod': 'patients_list',
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'required': ['id, gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'Residence_type', 'avg_glucose_level', 'bmi', 'smoking_status', 'stroke'],
                'properties': {


                    'gender': {
                        'bsonType': 'string',
                        'enum': ['Male', 'Female', 'Other']
                    },
                    'age': {
                        'bsonType': 'double',
                        'minimum': 0,
                        'maximum': 120
                    },
                    'hypertension': {
                        'bsonType': 'int',
                        'enum': [0, 1]
                    },
                    'heart_disease': {
                            'bsonType': 'int',
                            'enum': [0, 1]
                    },
                    'ever_married': {
                        'bsonType': 'string',
                        'enum': ['Yes', 'No']
                    },
                    'work_type': {
                        'bsonType': 'string'
                    },
                    'Residence_type': {
                        'bsonType': 'string',
                        'enum': ['Rural', 'Urban']
                    },
                    'avg_glucose_level': {
                        'bsonType': ['double', 'int'],  # to accept both int and double ['double', 'init']
                        'minimum': 0
                    },
                    'bmi': {
                        'bsonType': ['double', 'int'],  # to accept both int and double ['double', 'init']
                        'minimum': 10,
                        'maximum': 50
                    },
                    'smoking_status': {
                        'bsonType': 'string',
                        'enum': ['formerly smoked', 'never smoked', 'smokes', 'Unknown']
                    },
                    'stroke': {
                        'bsonType': ['double', 'int'],  # to accept both int and double ['double', 'init']
                        'minimum': 0,
                        'maximum': 1
                    }
                }
            }
        }
    })


def init_databases():
    # Initialize both databases and show any errors
    try:
        setup_sqlite()
        print("SQLite database setup complete")

        setup_mongodb()
        print("MongoDB setup complete")

    except Exception as e:
        print(f"Error setting up databases: {e}")
        raise e  # Re-raise the error so the app knows something went wrong


# Database connection

def get_db_connection():
    # Connect to SQLite - used for user accounts
    conn = sqlite3.connect('user_base.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_mongodb_connection():
    # Connect to MongoDB - used for patient data
    client = MongoClient('mongodb://localhost:27017/')
    db = client['stroke_management']
    return db

from pymongo import MongoClient

def setup_mongodb():
    client = MongoClient('mongodb://localhost:27017/')  # connection string
    db = client['Stroke_management']  #database name

    if 'patients_list' in db.list_collection_names():
        db['patients_list'].drop()
        print("collection 'patients_list' dropped.")

        db.create_collection('patients_list')
        print("Collection 'patients_list' created successfully.")

# Only run database setup if this file is ran directly
if __name__ == "__main__":
    init_databases()