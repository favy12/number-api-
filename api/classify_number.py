# api/classify_number.py

import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import math
import requests
from collections import OrderedDict

# Load configuration from environment variables
NUMBERS_API_URL = os.getenv("NUMBERS_API_URL", "http://numbersapi.com")
HOST = os.getenv("FLASK_HOST", "0.0.0.0")
PORT = int(os.getenv("FLASK_PORT", 80))

# Create Flask app
app = Flask(__name__)
CORS(app)

# (Optional) Custom JSON encoder if you want arrays on one line.
class CustomJSONEncoder(json.JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, (list, tuple)):
            if all(isinstance(x, str) for x in obj):
                return '[' + ', '.join(f'"{x}"' for x in obj) + ']'
        return super().encode(obj)

def custom_json_dumps(obj, **kwargs):
    return json.dumps(obj, cls=CustomJSONEncoder, **kwargs)

# Function to check if a number is prime.
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Function to check if a number is a perfect number.
def is_perfect(n):
    if n <= 0:
        return False
    if n == 1:
        return False
    sum_divisors = 1
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            sum_divisors += i
            if i != n // i:
                sum_divisors += n // i
    return sum_divisors == n

# Function to check if a number is an Armstrong number.
def is_armstrong(n):
    digits = str(n)
    power = len(digits)
    return sum(int(digit) ** power for digit in digits) == n

# Function to calculate the sum of the digits of a number.
def sum_of_digits(n):
    return sum(int(digit) for digit in str(abs(n)))

# Function to get a fun fact from Numbers API.
def get_fun_fact(n):
    try:
        url = f"{NUMBERS_API_URL}/{n}/math?json"
        fact_response = requests.get(url, timeout=3)
        if fact_response.status_code == 200:
            fact_data = fact_response.json()
            return fact_data.get("text", "No fun fact available.")
    except Exception:
        return "No fun fact available."
    return "No fun fact available."

# Define a default route for the root URL.
@app.route('/', methods=['GET'])
def index():
    return "Welcome to the Number Classification API! Use /api/classify-number?number=YOUR_NUMBER to classify a number."

# The main API route to classify our number.
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    num_param = request.args.get('number')
    
    if num_param is None:
        return jsonify({
            "number": "missing",
            "error": True
        }), 400

    try:
        # Convert input to float to handle integers, negatives, and floats.
        n_val = float(num_param)
    except ValueError:
        return jsonify({
            "number": num_param,
            "error": True,
            "message": "Invalid number format"
        }), 400

    # Convert the float to an integer for classification.
    n = int(n_val)

    properties = []
    if is_armstrong(n):
        properties.append("armstrong")
    properties.append("even" if n % 2 == 0 else "odd")

    if is_armstrong(n):
        digits = str(n)
        power = len(digits)
        # Using the caret notation for clarity
        fun_fact = f"{n} is an Armstrong number because " + " + ".join(f"{d}^{power}" for d in digits) + f" = {n}"
    else:
        fun_fact = get_fun_fact(n)

    # Create the response dictionary.
    response_data = {
        "number": n,
        "is_prime": is_prime(n),
        "is_perfect": is_perfect(n),
        "properties": properties,
        "digit_sum": sum_of_digits(n),
        "fun_fact": fun_fact
    }

    # Return valid JSON using Flask's jsonify.
    return jsonify(response_data), 200

# Run the app on the configured host and port.
if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
