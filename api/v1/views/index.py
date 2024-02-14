#!/usr/bin/python3
"""Script that import app_views"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def api_status():
    """a function to return api status"""
    return jsonify({"status": "OK"})
