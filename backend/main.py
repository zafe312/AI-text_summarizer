import os
import logging
from app import App
from flask import Flask, request, jsonify, abort

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)

@app.route('/summarize', methods=["POST"])
def summarize():
    try:
        logging.info("Received request at /summarize endpoint")
        
        data = request.get_json()
        if not data:
            logging.warning("Missing JSON payload in request.")
            return jsonify({"error": "Missing JSON payload"}), 400

        content = data.get('content')

        if not content:
            logging.warning(f"No content found: content={content}.")
            return jsonify({
                "error": "Missing content."
            }), 400

        logging.info(f"Generating responses: content={content}.")
        summary_app = App()
        summary, sentiment, insights = summary_app.run(content=content)

        if "Error" in summary:
            logging.error(f"Summarization failed: {summary}")
            return jsonify({"error": summary}), 500
        
        if "Error" in sentiment:
            logging.error(f"Sentiment analysis failed: {sentiment}")
            return jsonify({"error": sentiment}), 500
        
        if "Error" in insights:
            logging.error(f"Insights extraction failed: {insights}")
            return jsonify({"error": insights}), 500

        return jsonify({"summary": summary, "sentiment": sentiment, "insights": insights}), 200

    except Exception as e:
        logging.exception("Unexpected error in /summarize endpoint")
        return jsonify({"error": "Internal server error"}), 500

# Run the server
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)