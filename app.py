from flask import Flask, request, jsonify

app = Flask(__name__)

# Variable to store the payload of the last POST request
last_payload = None

@app.route('/api', methods=['POST'])
def api():
    global last_payload
    # Get JSON payload from the request
    last_payload = request.get_json()
    return jsonify({"message": "Payload received"}), 200

@app.route('/')
def index():
    if last_payload is None:
        return jsonify({"message": "No POST requests received yet."}), 200
    return jsonify(last_payload), 200

if __name__ == '__main__':
    app.run()
