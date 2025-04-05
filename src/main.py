from flask import Flask, request, jsonify
import json
import os
from src.api.routes import api_routes

app = Flask(__name__)

app.register_blueprint(api_routes)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
