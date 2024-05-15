from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient, ASCENDING
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3001"}}, supports_credentials=True)

with open('config.json', 'r') as file:
    config = json.load(file)

# MongoDB setup
client = MongoClient(config['log_settings']['db_uri'])
db = client[config['log_settings']['db_name']]
log_collection = db[config['log_settings']['collection_name']]


# Configure log files dynamically
loggers = {}

def get_logger(file_name):
    if file_name not in loggers:
        logger = logging.getLogger(file_name)
        logger.setLevel(logging.INFO)
        handler = RotatingFileHandler(file_name, maxBytes=5000, backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        loggers[file_name] = logger
    return loggers[file_name]

@app.route("/", methods=['POST'])
def insert_log():
    try:
        logs = request.json
        for log_entry in logs:
            # Insert into MongoDB
            log_collection.insert_one(log_entry)

            # Log to respective file
            logger = get_logger(log_entry["metadata"]["source"])
            logger.log(logging.getLevelName(log_entry["level"].upper()), log_entry["log_string"])

        return jsonify({"success": True, "insertedCount": len(logs)})
    except Exception as e:
        print(e)
        return jsonify({"msg": "Internal Server Error"}), 500
    

#tested using postman with approximately 50 json log data
@app.route("/query", methods=['POST'])
def query_logs():
    data = request.json
    level = data.get('level')
    log_string = data.get('log_string')
    source = data.get('source')
    startDate = data.get('startDate')
    endDate = data.get('endDate')

    query = {}
    if level:
        query['level'] = {'$regex': level, '$options': 'i'}
    if log_string:
        query['log_string'] = {'$regex': log_string, '$options': 'i'}
    if source:
        query['metadata.source'] = {'$regex': source, '$options': 'i'}
    if startDate and endDate:
        start_date = datetime.datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%SZ")
        end_date = datetime.datetime.strptime(endDate, "%Y-%m-%dT%H:%M:%SZ")
        query['timestamp'] = {'$gte': start_date, '$lt': end_date}

    try:
        results = list(log_collection.find(query))
        for result in results:
            result['_id'] = str(result['_id'])  # Convert ObjectId to string for JSON serialization
        return jsonify(results)
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error while fetching data"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=3000)
