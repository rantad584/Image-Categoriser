
from flask import Flask, request
import numpy as np
import tensorflow as tf
from tensorflow import keras
import json
from base64 import b64decode
from io import BytesIO
from PIL import Image

app = Flask(__name__)
model = keras.models.load_model('recycling_model.keras')
class_names = [
 'Carton',
 'Organic Waste',
 'Wood',
 'battery',
 'cardboard',
 'clothes',
 'glass',
 'metal',
 'paper',
 'plastic',
 'shoes',
 'trash']

def predict_category(image_string):
    try:
        image = Image.open(BytesIO(b64decode(image_string))) # decode base64 encoded image and create up PIL instance

        # Resize and preprocess the image
        image = tf.expand_dims(keras.utils.img_to_array(image.resize((256, 256))), axis=0)

        prediction = model.predict(image)
        score = tf.nn.softmax(prediction[0])

        return json.dumps(
            {
                'category': class_names[np.argmax(score)],
                'confidence:': f'{np.max(score) * 100}%'
            }
        , indent=4)

    except Exception as e:
        print(f'Exception {e}')

# Accept post requests to this route
@app.route('/upload', methods=['POST'])
def main():
    obj = request.get_json() # get request and convert to python object

    return predict_category(obj['image'])

if __name__ == '__main__':
    app.run(host='0.0.0.0')
