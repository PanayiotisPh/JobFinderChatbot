import json
import pymongo
import glassdoor.glassdoor_scrapper as glassdoorScrapper
import ergodotisi.ergodotisi_scrapper as ergodotisiScrapper

def upload_data(ergodotisi_filename, glassdoor_filename):
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017", 
                                username='root',
                                password='password')
    db = client["mongodb"]
    collection = db["jobs"]

    # Delete previously inserted data
    collection.delete_many({})

    # Read and insert the large JSON file
    try:
        with open(f'scrapper\\ergodotisi\\job_data\\{ergodotisi_filename}', 'r') as file:
            file_data = json.load(file)
            
            if isinstance(file_data, list):
                for document in file_data:
                    url = document.get('URL')
                    if url:
                        document['_id'] = url  # Use URL as the _id
                collection.insert_many(file_data)
            else:
                url = file_data.get('URL')
                if url:
                    file_data['_id'] = url  # Use URL as the _id
                collection.insert_one(file_data)

        # Close the MongoDB connection
    except Exception as e:
        print(f"An error occurred: {e}")
    
    try:
        with open(f'scrapper\\glassdoor\\job_data\\{glassdoor_filename}', 'r') as file:
            file_data = json.load(file)
            
            if isinstance(file_data, list):
                for document in file_data:
                    url = document.get('URL')
                    if url:
                        document['_id'] = url  # Use URL as the _id
                collection.insert_many(file_data)
            else:
                url = file_data.get('URL')
                if url:
                    file_data['_id'] = url  # Use URL as the _id
                collection.insert_one(file_data)

        # Close the MongoDB connection
        client.close()
    except Exception as e:
        print(f"An error occurred: {e}")


glassdoor_filename = glassdoorScrapper.run()
ergodotisi_filename = ergodotisiScrapper.run()
upload_data(ergodotisi_filename, glassdoor_filename)