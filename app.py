from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import CORS
from quiz_generator import get_quiz_for_topic

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_quiz', methods=['POST'])
def get_quiz():
    data = request.get_json()
    topic = data.get('topic')
    if not topic:
        return jsonify({"error": "Please provide a topic in the request body."}), 400
    result = get_quiz_for_topic(topic)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
