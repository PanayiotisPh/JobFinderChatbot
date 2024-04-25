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
import PyPDF2
import docx


app = Flask(__name__)
CORS(app)
secret_key = secrets.token_urlsafe(32)
app.config['JWT_SECRET_KEY'] = "BSOXl7U6DC8BA8M22QLE55d6Y-8S0TSFlRIge5_inuQ"
jwt = JWTManager(app)

def initialize_connection_users():
    client = pymongo.MongoClient("mongodb://localhost:27018", 
                                username='root',
                                password='password')
    db = client["mongodbUsers"]
    collection = db["users"]
    return collection , client

def initialize_connection_jobs():
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
