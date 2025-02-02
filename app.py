# Import the necessary tools from Flask and others
import json
import os
from flask import Flask, request
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

# Custom JSON encoder to keep arrays on one line
class CustomJSONEncoder(json.JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, (list, tuple)):
            if all(isinstance(x, str) for x in obj):  # Check if it's a list of strings
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

# Function to check if number is a perfect number.
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

# Function to get a fun fact from Numbers API
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

# The main API route to classify our number
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    num_param = request.args.get('number')
    
    if num_param is None:
        return app.response_class(
            response=json.dumps({
                "number": "missing",
                "error": True
            }, indent=4),
            status=400,
            mimetype='application/json'
        )

    try:
        n = int(num_param)
    except ValueError:
        return app.response_class(
            response=json.dumps({
                "number": num_param,
                "error": True
            }, indent=4),
            status=400,
            mimetype='application/json'
        )

    properties = []
    if is_armstrong(n):
        properties.append("armstrong")
    properties.append("even" if n % 2 == 0 else "odd")

    if is_armstrong(n):
        digits = str(n)
        power = len(digits)
        fun_fact = f"{n} is an Armstrong number because {' + '.join(f'{d}^{power}' for d in digits)} = {n}"
    else:
        fun_fact = get_fun_fact(n)

    # Initialize response first
    response_str = '''{
    "number": %d,
    "is_prime": %s,
    "is_perfect": %s,
    "properties": %s,
    "digit_sum": %d,  // sum of its digits
    "fun_fact": "%s"
}''' % (
        n,
        str(is_prime(n)).lower(),
        str(is_perfect(n)).lower(),
        json.dumps(properties),
        sum_of_digits(n),
        fun_fact
    )

# Return formatted JSON response
    return app.response_class(
        response=response_str,
        status=200,
        mimetype='application/json'
    )

# Run this app on configured host and port
if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
