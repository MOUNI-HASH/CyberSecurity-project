from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

TICKET_FILE = 'tickets.csv'

# Create CSV file with headers if it doesn't exist
if not os.path.exists(TICKET_FILE):
    with open(TICKET_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ticket_id", "description", "status"])

@app.route('/create_ticket', methods=['POST'])
def create_ticket():
    data = request.json
    description = data.get("description", "No description provided")
    # For simplicity, ticket_id is just the number of lines in CSV
    with open(TICKET_FILE, mode='r') as file:
        ticket_count = sum(1 for row in file)
    ticket_id = ticket_count  # header counts as one, so first ticket is ID 1
    with open(TICKET_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ticket_id, description, "open"])
    return jsonify({"message": "Ticket created", "ticket_id": ticket_id}), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)

