from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json()
    text = data.get('text')

    # Here you would call the LLM API to process the text and get the credibility assessment
    # Replace this with your actual logic to interact with the LLM API

    # For demonstration, let's assume the LLM API returns a fake assessment
    assessment = "Fake News" if "fake" in text.lower() else "Not Fake News"

    return jsonify({'assessment': assessment})

if __name__ == '__main__':
    app.run(debug=True)