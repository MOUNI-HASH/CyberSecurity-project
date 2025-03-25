from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Enable CORS
import csv
import os
import requests

app = Flask(__name__)
CORS(app)  # ✅ Allow frontend requests

TICKET_FILE = 'tickets.csv'
AI_AGENT_ENDPOINT = "http://127.0.0.1:5002/analyze_threat"

# Create CSV file if it doesn't exist
if not os.path.exists(TICKET_FILE):
    with open(TICKET_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ticket_id", "description", "status"])  # Header row

@app.route('/create_ticket', methods=['POST'])
def create_ticket():
    """ Creates a new ticket and appends it to the CSV file. """
    data = request.json
    description = data.get("description", "No description provided")

    with open(TICKET_FILE, mode='r') as file:
        ticket_count = sum(1 for row in file)

    ticket_id = ticket_count  # First ticket starts at ID 1

    with open(TICKET_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ticket_id, description, "open"])

    print(f"✅ Ticket {ticket_id} created: {description}")  

    return jsonify({
        "message": "Ticket created successfully",
        "ticket_id": ticket_id
    }), 200

@app.route('/ticket_status/<int:ticket_id>', methods=['GET'])
def get_ticket_status(ticket_id):
    """ Fetches the status of a ticket based on its ID. """
    with open(TICKET_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row

        for row in reader:
            if row[0] == str(ticket_id):
                return jsonify({"ticket_id": ticket_id, "status": row[2]}), 200

    return jsonify({"error": "Ticket not found"}), 404

if __name__ == '__main__':
    app.run(port=5001, debug=True)



