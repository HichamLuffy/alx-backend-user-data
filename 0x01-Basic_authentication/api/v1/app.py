#!/usr/bin/env python3
""" Route module for the API"""


from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    host = os.getenv('API_HOST', '127.0.0.1')
    port = int(os.getenv('API_PORT', 5000))
    print(f"Running on {host}:{port}")
    app.run(host=host, port=port)
