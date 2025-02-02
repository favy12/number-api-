# Import the necessary tools from Flask and others
from flask import Flask, request, jsonify
from flask_cors import CORS
import math
import requests
import json
from collections import OrderedDict

# Create a Flask app
app = Flask(__name__)
CORS(app)  # This makes sure our API can be used by websites from other places

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

# Function to get a fun fact from Numbers API
def get_fun_fact(n):
    try:
        url = f"http://numbersapi.com/{n}/math?json"
        fact_response = requests.get(url, timeout=3)
        if fact_response.status_code == 200:
            fact_data = fact_response.json()
            return fact_data.get("text", "No fun fact available.")
    except Exception:
        return "No fun fact available."
    return "No fun fact available."

# The main API route to classify our number.
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    # Get the number from the URL (like: /api/classify-number?number=371)
    num_param = request.args.get('number')
    if num_param is None:
        return jsonify({"error": True, "message": "Missing parameter 'number'"}), 400

    try:
        n = int(num_param)
    except ValueError:
        return jsonify({"number": num_param, "error": True, "message": "Invalid number format"}), 400
    
    # Initialize response OrderedDict first
    response = OrderedDict([
        ("number", n),
        ("is_prime", is_prime(n)),
        ("is_perfect", is_perfect(n)),
        ("properties", []),
        ("sum_of_digits", sum_of_digits(n)),
        ("note", "Sum of its digits"),
        ("fun_fact", "")
    ])

    # Check if it is an Armstrong number first (to ensure order)
    if is_armstrong(n):
        response["properties"].append("armstrong")

    # Check if number is even or odd
    response["properties"].append("even" if n % 2 == 0 else "odd")

    # Generate Armstrong fun fact if applicable
    if "armstrong" in response["properties"]:
        superscript_digits = "⁰¹²³⁴⁵⁶⁷⁸⁹"  # Unicode superscripts
        armstrong_exp = " + ".join(f"{d}{superscript_digits[len(str(n))]}" for d in str(n))
        response["fun_fact"] = f"{n} is an Armstrong number because {armstrong_exp} = {n}"

    # If no Armstrong fun fact, fetch from Numbers API
    if not response["fun_fact"]:
        response["fun_fact"] = get_fun_fact(n)

    # Return formatted JSON response
    return app.response_class(
        response=json.dumps(response, indent=4),
        status=200,
        mimetype='application/json'
    )

# Run the app on port 80
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
