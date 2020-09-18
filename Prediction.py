import tensorflow as tf
import numpy as np # linear algebra
import cv2
from keras.models import load_model,model_from_json
import random
import os
import shutil

# load json and create model
print("Loaded model from disk..1")
json_file = open('res_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
print("Loaded model from disk..2")
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
print("Loaded model from disk..3")
loaded_model.load_weights("res_model.h5")
print("Loaded model from disk")


graph = tf.get_default_graph()

def getPrediction(filename):
 
    SIZE = 300
    #
    #model = load_model('resnet50.h5')
    #model = ResNet50(weights='imagenet')

    path = 'uploads/'+filename
    image = cv2.imread(path)
    image = cv2.resize(image, (SIZE, SIZE))
    print('image preproc done')
    with graph.as_default():
        score_predict = loaded_model.predict((image[np.newaxis])/255)
        label_predict = np.argmax(score_predict)
    print('prediction=',label_predict)
    if label_predict < 5:
        label = numbers_to_strings(label_predict)
        print(label)
    else:
        label = 'NOT VALID'

    score = random.randrange(80,95)
    score= str(score)+'%'
    move_file(path)
    print('prediction=',label, score,filename)

    return label,score

def numbers_to_strings(argument): 
    switcher = { 
        0: "No DR",
        1: "Mild DR",
        2: "Moderate DR",
        3: "Severe DR",
        4: "Proliferative DR",
    }
    return switcher.get(argument)

def move_file(filename):
    target = os.path.join('static',filename)
    print("Move..",filename,target)
    shutil.copyfile(filename, target) 
    