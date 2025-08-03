# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from database import get_client_by_id  # ✅ using your existing MySQL logic

# app = Flask(__name__)
# CORS(app)  # ✅ allow access from Flutter app

# @app.route("/", methods=["GET"])
# def home():
#     return "✅ Real Estate API is running"

# @app.route("/client-info", methods=["GET"])
# def get_client_info():
#     client_id = request.args.get("id")
#     pin = request.args.get("pin")

#     if not client_id or not pin:
#         return jsonify({"success": False, "message": "Missing ID or PIN"}), 400

#     client = get_client_by_id(client_id)

#     if client and client["pin"] == pin:
#         return jsonify({"success": True, "data": client})
#     else:
#         return jsonify({"success": False, "message": "Invalid ID or PIN"}), 404

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)

print("✅ File loaded")  # STEP 1

from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_client_by_id

app = Flask(__name__)
CORS(app)

print("✅ Flask app initialized")  # STEP 2

@app.route("/", methods=["GET"])
def home():
    print("🔁 GET / called")  # STEP 3
    return "✅ Real Estate API is running"

@app.route("/client-info", methods=["GET"])
def get_client_info():
    print("🔍 /client-info called")  # STEP 4
    client_id = request.args.get("id")
    pin = request.args.get("pin")
    print(f"🧾 Received: id={client_id}, pin={pin}")  # STEP 5

    if not client_id or not pin:
        return jsonify({"success": False, "message": "Missing ID or PIN"}), 400

    try:
        client = get_client_by_id(client_id)
        print(f"🧠 DB Response: {client}")  # STEP 6
    except Exception as e:
        print(f"❌ Error in get_client_by_id: {e}")
        return jsonify({"success": False, "message": "Server error"}), 500

    if client and client["pin"] == pin:
        return jsonify({"success": True, "data": client})
    else:
        return jsonify({"success": False, "message": "Invalid ID or PIN"}), 404

if __name__ == "__main__":
    print("🚀 Starting Flask API...")  # STEP 7
    app.run(host="0.0.0.0", port=5000, debug=True)
