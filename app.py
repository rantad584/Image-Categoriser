
from flask import Flask, request
import json

app = Flask(__name__)

# Accept post requests to this route
@app.route('/upload', methods=['POST'])
def main():
    obj = request.get_json() # get request and convert to python object

    file = obj['image']

    return json.dumps(
        {
            'class': 'glass',
            'confidence:': '80%',
            'filename': file
        }
    , indent=4)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
