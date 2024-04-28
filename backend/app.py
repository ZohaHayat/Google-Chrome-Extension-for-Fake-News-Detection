from flask import Flask, request, jsonify
from llm import get_response


app = Flask(__name__)

@app.route('/process_text', methods=['POST'])
def process_text():
    text = request.json['text']
    processed_text = get_response(text)  # Example processing
    return jsonify(processed_text)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
