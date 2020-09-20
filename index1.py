from flask import Flask, render_template, request, redirect, flash, url_for
import urllib.request
from werkzeug.utils import secure_filename
import numpy as np # linear algebra
import cv2
from keras.models import load_model,model_from_json;
import tensorflow as tf
import os
from flask import Flask

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

graph = tf.get_default_graph()

json_file = open('res_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
print("Loaded model from disk..1")
loaded_model  = model_from_json(loaded_model_json)

loaded_model.load_weights("res_model.h5")
print("Loaded model from disk")

def getPrediction(filename): 
    SIZE = 300
    path = 'uploads/'+filename
    image = cv2.imread(path)
    image = cv2.resize(image, (SIZE, SIZE))
    print('image preproc done')
    with graph.as_default():
        score_predict = loaded_model.predict((image[np.newaxis])/255)
        label1 = np.argmax(score_predict)
    label = str(label1)
    print('prediction=',label)

    return label

@app.route('/')
def index():
    return render_template('index_test.html')



@app.route('/', methods=['GET','POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            #return 'TEST1'
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            #return 'TEST2'
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            #getPrediction(filename)
            label = getPrediction(filename)
            print('prediction =',label)
            flash(label)
            #flash(acc)
            flash(filename)
            return redirect('/')

#,threaded=True
if __name__ == "__main__":
    app.run(port=5002)
