from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

CLIENT_ID = "................."
CLIENT_SECRET = "............................."
THING_ID = "...................................."
PROPERTY_ID = ".................................."

def get_token():
    url = "https://api2.arduino.cc/iot/v1/clients/token"

    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "audience": "https://api2.arduino.cc/iot"
    }

    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

@app.route("/control", methods=["POST"])
def control_light():
    room = request.json.get("room")

    if room not in ["living room", "bathroom", "closet"]:
        return jsonify({"success": False, "error": "Invalid room"})

    token = get_token()

    url = f"https://api2.arduino.cc/iot/v2/things/{THING_ID}/properties/{PROPERTY_ID}/publish"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "value": room
    }

    response = requests.put(url, headers=headers, json=payload)

    if response.status_code in [200, 204]:
        return jsonify({"success": True, "room": room})
    else:
        return jsonify({
            "success": False,
            "status": response.status_code,
            "response": response.text
        })

if __name__ == "__main__":
    app.run(debug=True)