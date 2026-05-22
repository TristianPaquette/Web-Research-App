"""
app.py - Flask backend for the AI Web Research app.
"""

from dotenv import load_dotenv

# Load .env before importing agent.
# This matters because your agent files need the API keys.
load_dotenv()

from flask import Flask, jsonify, request
from agent import research


app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, world! Flask is working."


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    question = (data or {}).get("question", "").strip()

    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    try:
        result = research(question)
        return jsonify(result)

    except Exception as e:
        app.logger.exception("research() failed")
        return jsonify({"error": f"Something went wrong: {e}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)