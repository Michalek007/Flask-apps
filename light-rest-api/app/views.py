from flask import render_template, url_for, request, redirect, jsonify
from app import app


@app.route("/", methods=['POST', 'GET'])
def base():
    return render_template('base.html')
