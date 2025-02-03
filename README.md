# Number Classification API

This is a simple Flask-based API that classifies a number by checking whether it is prime, perfect, Armstrong, even, or odd. It also provides a fun fact for the number using the Numbers API.

## Features

- **Prime Check**: Checks if a number is prime.
- **Perfect Number Check**: Checks if a number is a perfect number.
- **Armstrong Number Check**: Checks if a number is an Armstrong number.
- **Even/Odd Check**: Determines if a number is even or odd.
- **Fun Fact**: Provides a fun fact about the number using the Numbers API.

## Requirements

- Python 3.x
- Flask
- Flask-CORS
- Requests

You can install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```
Create a requirements.txt file with the following content:
Flask==2.1.1
Flask-CORS==3.1.1
requests==2.26.0

## Running the Application
Activate the Virtual Environment
If you haven't created a virtual environment yet, you can create one using the following command:

```bash
python -m venv flaskenv
```
Then activate it:


```
source flaskenv/bin/activate
```

Run the Flask Application
After activating the virtual environment and installing the required dependencies, run the Flask application with:

```bash
FLASK_APP=app.py flask run --host=0.0.0.0 --port=80
```
This will start the development server on http://0.0.0.0:80.

--

## API Endpoints
### 1. GET /api/classify-number
This endpoint takes a number as a query parameter and returns a classification of that number.

Request Format:
```bash
GET /api/classify-number?number=<number>
```
Response Format:

```json
{
  "number": <number>,
  "is_prime": <true/false>,
  "is_perfect": <true/false>,
  "properties": ["even" or "odd", "armstrong"],
  "digit_sum": <sum_of_digits>,
  "fun_fact": "<fun_fact>"
}
```
Example:

Request:

typescript

GET /api/classify-number?number=28
Response:

json
Copy
Edit
{
  "number": 28,
  "is_prime": false,
  "is_perfect": true,
  "properties": ["even", "perfect"],
  "digit_sum": 10,
  "fun_fact": "28 is a perfect number because the sum of its divisors (1, 2, 4, 7, 14) equals 28."
}
Deployment
This API is deployed on AWS and is publicly accessible. Make sure to update your environment variables if necessary when deploying.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Contributing
Fork the repository.
Create a new branch (feature-branch).
Commit your changes.
Push to the branch.
Open a Pull Request.
If you encounter any issues or have suggestions, feel free to create an issue or contact the project owner.

