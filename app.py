from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import json
import os
import sys
from pathlib import Path 

app = Flask(__name__)
CORS(app, origins="https://solutionscentaurus.netlify.app")

@app.route('/executar_script', methods=['POST', 'GET'])
def executar_script():
    file = request.files['file']
    try:
        result = subprocess.run([sys.executable], {file.py}, capture_output=True, text=True, check=True)
        if result:
            print("File execute with sucessful")
    except:
        print("Not possible execute file")
        
if __name__ == '__main__':
    app.run(debug=True)