from flask import Flask, request, jsonify
from flask_cors import CORS
from queryOpenAI import GetResult

app = Flask(__name__)
CORS(app)

@app.route('/question', methods=['POST'])
def question_answer():
    data = request.json
    query = data.get('question')

    if not query:
        return jsonify({'error': 'Please provide a question in the request body.'}), 400
    
    result = GetResult(query)
    return jsonify({'answer': result})

if __name__ == '__main__':
    print("Starting flask app")
    app.run(port="5000")