import os
import pandas as pd
from pymongo import MongoClient

from app import patients_list


# MongoDB connection
def connect_to_mongo():
    mongo_uri = "mongodb://localhost:27017"  # mongo uri
    client = MongoClient(mongo_uri)
    return client


# Insert CSV data into MongoDB
def load_csv_to_mongo(stroke_management=None):
    try:
        # Path to CSV
        csv_path = os.path.join(os.path.dirname(__file__), 'dataset.csv')

        # Check if CSV file exists
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")


        # Read CSV using tab as the delimiter
        df = pd.read_csv(csv_path, delimiter='\t')
        print(df.head())

        print("CSV file loaded successfully!")

        # Connect to MongoDB
        client = connect_to_mongo()
        db = client['stroke_management']  # database name
        collection = db['patients_list']  # collection name

        # Convert DataFrame to list of dictionaries and insert into MongoDB
        data_dict = df.to_dict(orient='records')
        collection.insert_many(data_dict)
        print(f"Data successfully inserted into '{collection.name}' collection in '{db.name}' database.")

        # Close connection
        client.close()

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")


# Run the function
if __name__ == "__main__":
    load_csv_to_mongo()