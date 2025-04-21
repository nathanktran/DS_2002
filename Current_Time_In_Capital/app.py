from flask import Flask, request, jsonify
from datetime import datetime
import pytz

app = Flask(__name__)

AUTHORIZED_TOKENS = {"ilikehamburgers6144"}

CAPITAL_TIMEZONES = {
    "Washington": "America/New_York",
    "London": "Europe/London",
    "Tokyo": "Asia/Tokyo",
    "Paris": "Europe/Paris",
    "Canberra": "Australia/Sydney",
    "Ottawa": "America/Toronto",
    "Brasília": "America/Sao_Paulo",
    "New Delhi": "Asia/Kolkata"
}

@app.route('/')
def home():
    return "Welcome to my Capital Time API"

@app.route('/api/time')
def get_time():
    token = request.args.get('token')
    city = request.args.get('city')

    if not token or token not in AUTHORIZED_TOKENS:
        return jsonify({"error": "Please provide a valid token."}), 401

    if not city:
        return jsonify({"error": "Missing city parameter"}), 400

    timezoneName = CAPITAL_TIMEZONES.get(city)
    if not timezoneName:
        return jsonify({"error": f"City '{city}' not found."}), 404

    timezone = pytz.timezone(timezoneName)
    now = datetime.now(timezone)
    time_str = now.strftime('%Y-%m-%d %H:%M:%S')
    offset = now.strftime('%z')

    return jsonify({
        "city": city,
        "current_time": time_str,
        "utc_offset": offset
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
