from flask import Flask, request, jsonify
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

app = Flask(__name__)

@app.route("/")
def home():
    return "📞 Welcome to Mobile Number Info API! Use /number?phone=+919876543210"

@app.route("/number", methods=["GET"])
def number_info():
    phone = request.args.get("phone", "")
    try:
        number = phonenumbers.parse(phone)
        if not phonenumbers.is_valid_number(number):
            return jsonify({"error": "Invalid phone number"})

        info = {
            "input": phone,
            "valid": True,
            "number_type": str(phonenumbers.number_type(number)),
            "country": geocoder.description_for_number(number, "en"),
            "carrier": carrier.name_for_number(number, "en"),
            "time_zones": timezone.time_zones_for_number(number)
        }
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
