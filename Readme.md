# Log Query and Ingestion API

This project is a Flask-based API that ingests and queries log data stored in MongoDB. It supports dynamic logging to files and MongoDB based on incoming request data.

## Features

- Ingest logs via API and store in MongoDB.
- Query logs dynamically based on various parameters like level, message, timestamp, etc.
- Log data is also written to files dynamically based on the source specified in the log data.

## Setup

To get this project up and running, follow these steps:

### Prerequisites

- Python 3.8 or higher
- MongoDB server or MongoDB Atlas account

### Installation
1. Navigate to the project directory:
2. Create a virtual environment:
python -m venv venv
3. Activate the virtual environment:
- Windows:
  ```
  venv\Scripts\activate
  ```
- MacOS/Linux:
  ```
  source venv/bin/activate
  ```
4. Install the required dependencies:
pip install -r requirements.txt


### Configuration

Ensure the MongoDB connection string in `app.py` is set to your MongoDB instance.

### Running the Application

Run the Flask application with the following command:
flask run


### Using the API

Use a tool like Postman to send POST requests to `http://localhost:3000/query` with appropriate JSON payloads to query or log data.


