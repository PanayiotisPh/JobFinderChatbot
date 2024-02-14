# webhook.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

rasa_server_url = "http://localhost:5005/webhooks/rest/webhook"  # Replace with your Rasa server URL

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    # Assuming the user's message is in the 'message' field
    user_message = data.get("message")

    # Forward the message to the Rasa server
    rasa_response = requests.post(rasa_server_url, json={"message": user_message}).json()

    return jsonify(rasa_response)

if __name__ == "__main__":
    app.run(port=5006)  # Choose any port you prefer
