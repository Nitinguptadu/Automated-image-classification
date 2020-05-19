import os
import sys

# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Some utilites
import numpy as np
from util import base64_to_pil
import base64
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient

from time import gmtime, strftime
from datetime import datetime
import pymongo 



# Declare a flask app
app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.oncosteam_server_image #Select the database
employee = db.employee #Select the collection name



# You can use pretrained model from Keras
# Check https://keras.io/applications/
from keras.applications.mobilenet_v2 import MobileNetV2
model = MobileNetV2(weights='imagenet')

print('Model loaded. Check http://127.0.0.1:5000/')


# Model saved with Keras model.save()
#MODEL_PATH = 'models/model2.weights.best_MobileNetV2_1.hdf5'

# Load your own trained model
#model = load_model(MODEL_PATH)
#model._make_predict_function()          # Necessary
#print('Model loaded. Start serving...')


def model_predict(img, model):
    img = img.resize((224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x, mode='tf')

    preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the image from post request
        img = base64_to_pil(request.json)
        
        

        # Save the image to ./uploads
        img.save("./uploads/image.png")
        
        
        with open("./uploads/image.png", "rb") as img_file:
            my_string = base64.b64encode(img_file.read())
        

        # Make prediction
        preds = model_predict(img, model)

        # Process your result for human
        pred_proba = "{:.3f}".format(np.amax(preds))    # Max probability
        pred1 = float(pred_proba)
        
       
        
        pred_class = decode_predictions(preds, top=1)   # ImageNet Decode
        image_name = str(pred_class[0][0][0])

        result = str(pred_class[0][0][1])               # Convert to string



        

        
        
        result = result.replace('_', ' ').capitalize()

        employee.insert({"Image_Name":image_name,"prediction":pred1, "prediction_prob":result,"base_64":my_string,"Date":datetime.now().strftime('%Y-%m-%d'),"Time":datetime.now().strftime('%H:%M:%S')})
     
        
        # Serialize the result, you can add additional fields
        return jsonify(result=result, probability=pred_proba)

    return None


if __name__ == '__main__':
    # app.run(port=5002, threaded=False)

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
