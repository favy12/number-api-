# Number Classification API

This project is a Flask-based API that classifies a number by checking its mathematical properties and returns a fun fact. The API determines if a given number is **prime**, **perfect**, **Armstrong**, and whether it is **even** or **odd**. It also calculates the **sum of its digits**.

The API is deployed on **Vercel** and uses a serverless function located at `/api/classify_number.py`.

---

## Project Structure

```
/your-root-folder
├── api
│   └── classify_number.py  # Flask API code
├── requirements.txt        # Dependencies
└── vercel.json            # Vercel configuration
```

---

## Features

- **Numeric Classification:**  
  - Checks if a number is **prime**, **perfect**, or an **Armstrong** number.
  - Determines if the number is **even** or **odd**.
  - Calculates the **digit sum**.

- **Fun Fact Retrieval:**  
  - Retrieves a fun fact about the number from the Numbers API.

- **Input Handling:**  
  - Accepts all valid numeric inputs (integers, negative numbers, and floating‑point values).  
  - Returns a `200` status code for valid inputs; returns `400` only when the input is missing or invalid.

- **CORS Enabled:**  
  - The API handles cross-origin requests.

---

## Requirements

- Python 3.x
- Flask
- Flask-CORS
- Requests
- Gunicorn (for production)

Install dependencies using:

```bash
pip install -r requirements.txt
```

A sample `requirements.txt`:

```ini
Flask==3.1.0
Flask-CORS==5.0.0
gunicorn==23.0.0
requests==2.32.3
```

---

## Running Locally

### Clone the Repository

```bash
git clone https://github.com/your-username/number-api.git
cd number-api
```

### Create and Activate a Virtual Environment

```bash
python -m venv flaskenv
# On Linux/macOS:
source flaskenv/bin/activate
# On Windows:
flaskenv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

Since your API file is located at `/api/classify_number.py`, run:

```bash
python api/classify_number.py
```

The app will run on the host and port specified in the environment variables (default is `0.0.0.0:80`).

### Test the Endpoint

Visit the following URL in your browser or via Postman:

```
http://localhost/api/classify-number?number=371
```

---

## API Specification

### Endpoint

```
GET /api/classify-number?number=<number>
```

### Success Response (`200 OK`)

For a valid input (e.g., `?number=371`), the API returns a JSON object like:

```json
{
  "number": 371,
  "is_prime": false,
  "is_perfect": false,
  "properties": ["armstrong", "odd"],
  "digit_sum": 11,
  "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371."
}
```

### Error Response (`400 Bad Request`)

For an invalid input (e.g., `?number=alphabet`), the API returns:

```json
{
  "number": "alphabet",
  "error": true,
  "message": "Invalid number format"
}
```

---

## Deployment on Vercel

This project is deployed on **Vercel** without changing the existing structure. The Vercel configuration (`vercel.json`) routes requests to the Flask function.

### `vercel.json` Example

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/classify_number.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/classify-number",
      "dest": "/api/classify_number.py"
    }
  ]
}
```

### Steps to Deploy on Vercel

1. **Push Your Code to GitHub:**  
   Ensure your repository (with `/api/classify_number.py`, `requirements.txt`, and `vercel.json`) is on the main branch.

2. **Import the Repository into Vercel:**  
   - Log in to Vercel.
   - Click **New Project** and select your GitHub repository.
   - Vercel will detect the Python project using `requirements.txt` and `vercel.json`.

3. **Deploy:**  
   - Vercel will build and deploy your project. Your API endpoint will be available at:

   ```
   https://<your-app-name>.vercel.app/api/classify-number
   ```

4. **Test Your Deployed API:**  
   Visit the deployed URL with a valid query parameter:

   ```
   https://<your-app-name>.vercel.app/api/classify-number?number=371
   ```

---

## Code Overview

- **Input Validation:**  
  - The API converts the input to a float and then to an integer (if the value is whole) to handle all valid numeric values, including negatives and floats.

- **Classification Functions:**  
  - Functions `is_prime`, `is_perfect`, `is_armstrong`, and `sum_of_digits` determine the properties of the number.

- **Fun Fact Retrieval:**  
  - The function `get_fun_fact` calls the Numbers API to retrieve a fun fact about the number.

- **JSON Response:**  
  - The API builds a Python dictionary and returns it using Flask’s `jsonify()` for valid JSON output.

- **CORS:**  
  - Enabled via Flask-CORS, allowing cross-origin requests.

---

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. Ensure you follow the existing code style and document your changes.

---

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## Final Notes

- **Testing:**  
  - Ensure you test your API with various valid numbers (including negative and floating-point values) to confirm that a `200` status code is always returned for valid inputs.

- **Performance:**  
  - The API is designed to respond quickly (<500ms), but external API calls (for fun facts) may add slight delays.

- **Deployment:**  
  - The API is hosted on Vercel. If you need to update it, simply push changes to GitHub and Vercel will redeploy automatically.

---

**Happy coding!** 🚀

