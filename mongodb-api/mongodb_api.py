import pymongo
import json
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


def jaccard_similarity(set1, set2):
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union

def initialize_connection_users():
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27018", 
                                username='root',
                                password='password')
    db = client["mongodbUsers"]
    collection = db["users"]
    return collection , client

def initialize_connection_jobs():
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017", 
                                username='root',
                                password='password')
    db = client["mongodb"]
    collection = db["jobs"]
    return collection , client

@app.route('/users-data', methods=['GET'])
def get_all_users_data():
    collection, client = initialize_connection_users()
    data = list(collection.find({}))  # Query to fetch all documents
    client.close()
    return jsonify(data)

@app.route('/post-users', methods=['POST'])
def post_users():
    data = request.json
    collection, client = initialize_connection_users()
    collection.insert_many(data)
    client.close()
    return "Data inserted successfully"


@app.route('/data', methods=['GET'])
def get_all_data():
    collection, client = initialize_connection_jobs()
    data = list(collection.find({}))  # Query to fetch all documents
    client.close()
    return jsonify(data)

@app.route('/post-data', methods=['POST'])
def post_data():
    data = request.json
    collection, client = initialize_connection_jobs()
    collection.insert_many(data)
    client.close()
    return "Data inserted successfully"


@app.route('/get-results', methods=['POST'])
def get_results():
    data = request.json
    collection, client = initialize_connection_jobs()

    # Specify the desired "Location" value to match
    query_builder = {}
    # Check if the "Location" field in data is not empty
    if data.get("Location"):
        query_builder["Location"] = {"$in": data["Location"]}

    # Check if the "Company" field in data is not empty
    if data.get("Company") != "None":
        query_builder["Company"] = data["Company"]

    # Check if the "Employment Type" field in data is not empty
    if data.get("Employment Type"):
        query_builder["$or"] = [
            {"Employment Type": {"$in": data["Employment Type"]}},
            {"Employment Type": ""}
        ]

    # Check if the "Years of Exp" field in data is not empty
    if data.get("Years of Exp"):
        query_builder["$or"] = [
            {"Years of Exp": {"$lte": data["Years of Exp"]}},
            {"Years of Exp": "not given"}
        ]

    # Check if the "Education Level" field in data is not empty
    if data.get("Education Level"):
        query_builder["$or"] = [
            {"Education Level": {"$in": data["Education Level"]}},
            {"Education Level": ""}
        ]

    # Check if the "Education Type" field in data is not empty
    #if data.get("Education Type"):
    #    query_builder["Hard Skills"] = {"$in": data["Education Type"]}

    matching_entries = collection.find(query_builder)


    similar_documents = []

    for entry in matching_entries:
        document_hard_skills = set(entry.get("Hard Skills", []))  # Extract the "Hard Skills" field from the document
        document_soft_skills = set(entry.get("Soft Skills", []))  # Extract the "Soft Skills" field from the document
        hard_skill_similarity = jaccard_similarity(set(data["Hard Skills"]), document_hard_skills)
        soft_skill_similarity = jaccard_similarity(set(data["Soft Skills"]), document_soft_skills)
        if hard_skill_similarity >= 0.2 and soft_skill_similarity >= 0.2:  # Check if the similarity is at least 50%
            similar_documents.append(entry)
        elif hard_skill_similarity >= 0.3 and document_soft_skills == set([]):
            similar_documents.append(entry)
        elif soft_skill_similarity >= 0.2 and document_hard_skills == set([]):
            similar_documents.append(entry)
        elif document_soft_skills == set([]) and document_hard_skills == set([]):
            similar_documents.append(entry)


    matching_entries_list = list(similar_documents)
    urls = [entry['URL'] for entry in matching_entries_list]
    json_result = json.dumps(urls, default=str, indent=4)
    #print(json_result)    
    client.close()

    return json_result


if __name__ == '__main__':
    app.run(debug=True)
# Close the MongoDB connection
#get_results()

