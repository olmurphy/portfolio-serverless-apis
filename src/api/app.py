from flask import request, jsonify, Blueprint, jsonify
import json
import os
from dotenv import load_dotenv

# from get_latest_commit.handler import lambda_handler #import handler.

load_dotenv()

api_routes = Blueprint('api', __name__)

@api_routes.route('/repos/<owner>/<repo>/commits/latest', methods=['GET'])
def get_latest_commit(owner, repo):
    """Flask route to mimic Lambda behavior."""
    branch = request.args.get('branch', 'main')
    event = {'owner': owner, 'repo': repo, 'branch': branch}
    # result = lambda_handler(event)
    result = { 
        "statusCode": 200,
        "body": json.dumps({
            "commit_sha": "dummy_sha",
            "commit_timestamp": "dummy_timestamp"
        }),
    }
    return jsonify(json.loads(result['body'])), result['statusCode']
