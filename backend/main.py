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

        format = data.get('format')
        tone = data.get('tone')
        topic = data.get('topic')

        if not all([format, tone, topic]):
            logging.warning(f"Incomplete input: format={format}, tone={tone}, topic={topic}")
            return jsonify({
                "error": "Missing one or more required fields: format, tone, topic"
            }), 400

        logging.info(f"Generating quote: format={format}, tone={tone}, topic={topic}")
        quote_app = App()
        quote = quote_app.run(format=format, tone=tone, topic=topic)

        if "Error" in quote:
            logging.error(f"AI generation failed: {quote}")
            return jsonify({"error": quote}), 500

        return jsonify({"quote": quote}), 200

    except Exception as e:
        logging.exception("Unexpected error in /summarize endpoint")
        return jsonify({"error": "Internal server error"}), 500

# Run the server
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)