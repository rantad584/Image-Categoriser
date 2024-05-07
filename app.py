
from flask import Flask, request
import json

app = Flask(__name__)

# Accept post requests to this route
@app.route('/upload', methods=['POST'])
def main():
    if 'imageFile' not in request.files:
        return 'No file part', 400

    file = request.files['imageFile']

    if file.filename == '':
        return 'No selected file', 400

    return json.dumps(
        {
            'class': 'glass',
            'confidence:': '80%',
            'filename': file.filename
        }
    , indent=4)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
