from flask import Flask, request, send_file
import subprocess
import sys
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow frontend requests from another origin if needed

# Base directory of this file (important for serverless Vercel)
BASE_DIR = os.path.dirname(__file__)

# fixed PNG path
PNG_FILE = os.path.join(BASE_DIR, "molecules_grid.png")
GRAPH_SCRIPT = os.path.join(BASE_DIR, "Graph_Theory_Approach.py")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    formula = data.get("formula")
    if not formula:
        return "No formula provided", 400

    # run your existing Matrix_Generation.py script with formula and PNG_FILE as output
    # use full paths so Vercel can locate the script
    try:
        subprocess.run([sys.executable, GRAPH_SCRIPT, formula, PNG_FILE], check=True)
    except subprocess.CalledProcessError as e:
        return f"Subprocess failed: {e}", 500

    # return a simple response (frontend will reload the <img>)
    return "OK", 200

# optional: serve the PNG (if frontend wants direct URL)
@app.route("/molecules_grid.png", methods=["GET"])
def serve_png():
    if not os.path.exists(PNG_FILE):
        return "PNG not found", 404
    return send_file(PNG_FILE, mimetype="image/png")

if __name__ == "__main__":
    # only use this locally
    app.run(debug=True, host="127.0.0.1", port=5000)
