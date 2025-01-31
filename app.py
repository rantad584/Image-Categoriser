import json
import numpy as np
from base64 import b64decode
from io import BytesIO
from PIL import Image
from flask import Flask, request
import tensorflow as tf
from tensorflow import keras


app = Flask(__name__)
model = keras.models.load_model("recycling_model.keras")
class_names = [
    "Carton",
    "Organic Waste",
    "Wood",
    "battery",
    "cardboard",
    "clothes",
    "glass",
    "metal",
    "paper",
    "plastic",
    "shoes",
    "trash",
]


def predict_category(image_string):
    try:
        # decode base64 encoded image and create up PIL instance
        image = Image.open(BytesIO(b64decode(image_string))).convert("RGB")

        # Resize and preprocess the image
        image = tf.expand_dims(
            keras.utils.img_to_array(image.resize((256, 256))), axis=0
        )

        prediction = model.predict(image)
        scores = tf.nn.softmax(prediction[0])

        top_indices = np.argsort(scores)[-3:][::-1]

        result = {}
        for i in top_indices:
            result[class_names[i]] = np.round(scores[i].numpy() * 100, 2)

        return json.dumps(result, indent=4)

    except Exception as e:
        print(f"Exception {e}")


# Accept post requests to this route
@app.route("/", methods=["POST"])
def main():
    obj = request.get_json()  # get request and convert to python object
    return predict_category(obj["image"])


if __name__ == "__main__":
    app.run(host="0.0.0.0")
