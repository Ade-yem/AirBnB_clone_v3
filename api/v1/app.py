#!/usr/bin/python3
"""runs the flask app"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def not_found(error):
    """not found page"""
    return jsonify({"error": "Not found"})


app.teardown_appcontext


def close(error):
    """Closes the database again at the end of the request."""
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST') or '0.0.0.0'
    port = os.getenv('HBNB_API_PORT') or 5000
    app.run(host=host, port=port, threaded=True, debug=True)
