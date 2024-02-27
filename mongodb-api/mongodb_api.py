import pymongo
import json
from flask import Flask, request, jsonify
import requests
from werkzeug.security import check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import secrets
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId
import datetime


app = Flask(__name__)
CORS(app)
secret_key = secrets.token_urlsafe(32)
app.config['JWT_SECRET_KEY'] = "BSOXl7U6DC8BA8M22QLE55d6Y-8S0TSFlRIge5_inuQ"
jwt = JWTManager(app)

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
    client.close()

    return json_result

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    collection, client = initialize_connection_users()
    user = collection.find_one({"_id": email})

    if user['_id'] == email and check_password_hash(user['password'], password):
        # Create JWT token
        access_token = create_access_token(identity=user['_id'])
        client.close()
        return jsonify(access_token=access_token), 200
    
    client.close()
    return jsonify({"msg": "Bad username or password"}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    collection, client = initialize_connection_users()
    user = collection.find_one({"_id": email})

    if user:
        client.close()
        return jsonify({"message": "Email already in use"}), 400

    # Hash password and create new user
    hashed_password = generate_password_hash(password)
    data = {
        "_id": email,
        "username": username,
        "password": hashed_password,
        "results": []
    }
    collection.insert_one(data)

    client.close()
    return jsonify({"message": "Registration successful"}), 201

@app.route('/delete-users', methods=['DELETE'])
def delete_users():
    collection, client = initialize_connection_users()
    collection.delete_many({})
    client.close()
    return "Data deleted successfully"

@app.route('/api/messages', methods=['POST'])
@jwt_required()
def send_to_rasa():
    user_identity = get_jwt_identity()
    message_data = request.json.get('message')

    # Your Rasa endpoint
    rasa_endpoint = 'http://localhost:5005/webhooks/rest/webhook'

    # Forward the message to Rasa
    response = requests.post(rasa_endpoint, json={
        'sender': user_identity,  # Using the JWT identity as the sender
        'message': message_data,
    })

    if response.ok:
        # Return Rasa's response back to the client
        return jsonify(response.json()), 200
    else:
        return jsonify({'message': 'Failed to communicate with Rasa.'}), 500

@app.route('/get-username', methods=['GET'])
@jwt_required()
def get_username():
    user_identity = get_jwt_identity()
    collection, client = initialize_connection_users()
    user = collection.find_one({"_id": user_identity})
    client.close()
    return jsonify(user['username']), 200

@app.route('/save-chat', methods=['POST'])
@jwt_required()
def save_chat():
    user_email = get_jwt_identity()
    data = request.json
    chat = {
        "chatId": str(ObjectId()), # Generates a unique ID for the chat
        "date": datetime.datetime.utcnow().isoformat(),
        "messages": data['messages']
    }

    collection, client = initialize_connection_users()

    # Update the user's document to push the new chat into the results array
    collection.update_one(
        {"_id": user_email},
        {"$push": {"results": chat}}
    )

    client.close()

    return jsonify({"message": "Chat saved successfully"}), 200

@app.route('/api/sessions', methods=['GET'])
@jwt_required()
def get_sessions():
    collection, client = initialize_connection_users()
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_sessions = collection.find_one({"_id": current_user}, {"results": 1, "_id": 0})
    
    if not user_sessions:
        client.close()  # Ensure you close the client connection
        return jsonify({"msg": "No sessions found"}), 404

    client.close()  # Ensure you close the client connection
    return jsonify(user_sessions["results"]), 200

@app.route('/api/chat/<chatId>', methods=['GET'])
@jwt_required()
def get_chat_by_chatId(chatId):
    user_identity = get_jwt_identity()
    collection, client = initialize_connection_users()

    # Find the user document
    user_document = collection.find_one({"_id": user_identity})
    

    if user_document:
        # Iterate through the results to find the matching chatId
        for result in user_document.get('results', []):
            if result.get('chatId') == chatId:
                return jsonify(result.get('messages')), 200
        return jsonify({"msg": "Chat session not found"}), 404
    else:
        return jsonify({"msg": "User not found"}), 404

@app.route('/api/chat/<chatId>', methods=['DELETE'])
@jwt_required()
def delete_chat_by_chatId(chatId):
    user_identity = get_jwt_identity()
    collection, client = initialize_connection_users()

    # Attempt to update the user's document by pulling the chat session from the results array
    update_result = collection.update_one(
        {"_id": user_identity},
        {"$pull": {"results": {"chatId": chatId}}}
    )

    if update_result.modified_count > 0:
        # If the update modified a document, the chat session was successfully deleted
        return jsonify({"msg": "Chat session deleted successfully"}), 200
    else:
        # If no documents were modified, the chat session was not found for the user
        return jsonify({"msg": "Chat session not found"}), 404

@app.route('/api/change-password', methods=['POST'])
@jwt_required()
def change_password():
    user_identity = get_jwt_identity()
    collection, client = initialize_connection_users()
    data = request.json

    # Retrieve the user from the database
    user = collection.find_one({"_id": user_identity})  # Assuming username is unique and provided
    print(data["oldPassword"])

    if user:
        # Verify the old password
        if check_password_hash(user["password"], data["oldPassword"]):
            # Hash the new password before storing it
            hashed_password = generate_password_hash(data["newPassword"])

            # Update the user's password in the database
            collection.update_one(
                {"_id": user_identity},
                {"$set": {"password": hashed_password}}
            )

            return jsonify({"message": "Password updated successfully"}), 200
        else:
            return jsonify({"error": "Old password is incorrect"}), 400
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/api/change-username', methods=['POST'])
@jwt_required()
def change_username():
    user_identity = get_jwt_identity()
    collection, client = initialize_connection_users()
    data = request.json

    # Retrieve the user from the database
    user = collection.find_one({"_id": user_identity})  # Assuming username is unique and provided

    if user:
        # Verify the old username
        if user["username"].lower() == data["oldUsername"].lower():

            # Update the user's username in the database
            collection.update_one(
                {"_id": user_identity},
                {"$set": {"username": data["newUsername"]}}
            )

            return jsonify({"message": "Username updated successfully"}), 200
        else:
            return jsonify({"error": "Old username is incorrect"}), 400
    else:
        return jsonify({"error": "User not found"}), 404
    

if __name__ == '__main__':
    app.run(debug=True)
# Close the MongoDB connection
#get_results()

