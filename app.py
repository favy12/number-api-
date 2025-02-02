# Import the necessary tools from Flask and others
from flask import Flask, request, jsonify
from flask_cors import CORS
import math
import requests
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
        return jsonify({"number": num_param, "error": True}), 400
    
    # Initialize response OrderedDict first
    response = OrderedDict([
        ("number", n),
        ("is_prime", is_prime(n)),
        ("is_perfect", is_perfect(n)),
        ("properties", []),
        ("sum_of_digits", sum_of_digits(n)),
        ("fun_fact", "")
    ])


    # Check if number is even or odd
    response["properties"].append("even" if n % 2 == 0 else "odd")

    # Check if it is an Armstrong number
    if is_armstrong(n):
        response["properties"].append("armstrong")
        response["fun_fact"] = f"{n} is an Armstrong number because {' + '.join(f'{d}^{len(str(n))}' for d in str(n))} = {n}"

    # If no Armstrong number fact, fetch from Numbers API
    if not response["fun_fact"]:
        try:
            url = f"http://numbersapi.com/{n}/math?json"
            fact_response = requests.get(url, timeout=3)
            if fact_response.status_code == 200:
                fact_data = fact_response.json()
                response["fun_fact"] = fact_data.get("text", "No fun fact available.")
            else:
                response["fun_fact"] = "No fun fact available."
        except Exception:
            response["fun_fact"] = "No fun fact available."

   

    # Return our response as JSON
    return jsonify(response), 200

# Run the app if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True)
