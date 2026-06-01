from flask import Flask, request, jsonify
import csv
import os
from datetime import datetime

app = Flask(__name__)

# Store latest data for 3 patients
latest_data = {
    "patient1": {"button": 0, "motion": 0, "led": 0, "temp": None, "hum": None},
    "patient2": {"button": 0, "motion": 0, "led": 0, "temp": None, "hum": None},
    "patient3": {"button": 0, "motion": 0, "led": 0, "temp": None, "hum": None}
}

log_file = "patient_log.csv"

# Create CSV file with header if it doesn't exist
if not os.path.isfile(log_file):
    with open(log_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "patient_id", "button", "motion", "led", "temp", "hum"])

@app.route('/data', methods=['POST'])
def receive_data():
    global latest_data

    data = request.get_json()
    if data:
        patient_id = data.get("patient_id")

        if patient_id in latest_data:
            latest_data[patient_id] = data

            # Log data to CSV
            with open(log_file, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    patient_id,
                    data.get("button"),
                    data.get("motion"),
                    data.get("led"),
                    data.get("temp"),
                    data.get("hum")
                ])

            print("Received:", data)
            return jsonify({"status": "ok"}), 200

        else:
            return jsonify({"status": "error", "message": "Unknown patient_id"}), 400

    return jsonify({"status": "error", "message": "No data received"}), 400

@app.route('/latest', methods=['GET'])
def get_latest():
    return jsonify(latest_data)

@app.route('/')
def home():
    return "Flask server is running"

app.run(host='0.0.0.0', port=5000)