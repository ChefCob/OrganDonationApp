from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from New_Text_Document_5 import SecureOrganDonationNetwork  # Import your matching logic

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend connection

# Initialize Organ Donation System
network = SecureOrganDonationNetwork()

@app.route('/')
def home():
    return "Organ Donation Network Backend is Running!"

@app.route('/donor', methods=['POST'])
def register_donor():
    data = request.json
    try:
        donor_data = {
            "donor_id": data["donor_id"],
            "organ_type": data["organ_type"],
            "blood_type": data["blood_type"],
            "hla_typing": data["hla_typing"]
        }
        return jsonify({"message": "Donor registered successfully", "data": donor_data}), 200
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400

@app.route('/recipient', methods=['POST'])
def register_recipient():
    data = request.json
    try:
        recipient_data = {
            "recipient_id": data["recipient_id"],
            "organ_type": data["organ_type"],
            "blood_type": data["blood_type"],
            "hla_typing": data["hla_typing"]
        }
        return jsonify({"message": "Recipient registered successfully", "data": recipient_data}), 200
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400

@app.route('/match', methods=['POST'])
def process_match():
    data = request.json
    try:
        recipient_data = data["recipient"]
        donor_data = data["donor"]
        result = network.process_donation_request(recipient_data, donor_data)

        if result:
            return jsonify({"message": "Match found", "match_data": result}), 200
        else:
            return jsonify({"message": "No match found or suspicious activity detected"}), 200

    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400
@app.route('/favicon.ico')
def favicon():
    return ('', 204)  # Returns an empty response with HTTP 204 (No Content)
@app.route('/match', methods=['POST'])
def process_match_data():
    data = request.json
    try:
        recipient_data = data["recipient"]
        donor_data = data["donor"]

        # Process the matching request
        result = network.process_donation_request(recipient_data, donor_data)

        if result:
            return jsonify({"message": "Match found", "match_data": result}), 200
        else:
            return jsonify({"message": "No match found or suspicious activity detected"}), 200

    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400

if __name__ == '__main__':
    app.run(debug=True)
