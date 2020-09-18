from flask import Flask, render_template, abort,request,redirect,url_for,flash
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
#import driver
import Prediction
from werkzeug.utils import secure_filename
from Prediction import getPrediction
#import alerter
import os
 
 
app = Flask(__name__)

app.secret_key='5791628bb0b13ce0c676dfde280ba245' 
#UPLOAD_FOLDER = os.path.join('static', 'uploads')
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['SECRET_KEY']='5791628bb0b13ce0c676dfde280ba245'
 
# @app.route('/')
# def home():
#     return render_template('main.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about_team():
    return render_template('about-team.html')

@app.route('/contacts')
def contact():
    return render_template('contact.html')

@app.route('/services')
def service():
    return render_template('service.html')



@app.route('/predictionHome')
def predictionHome():
    return render_template('pred_entry.html')

@app.route('/predictionResult',methods=['POST','GET'])
def predictionResult():
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
            filename2 = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            file.save(filename2)
            patient=request.form['SEL']
            #getPrediction(filename)
            label, score = getPrediction(filename)
            flash(label)
            #flash(acc)
            flash(filename)
            return render_template('pred_result.html',Mae=label,Score=score,hist=filename2,patient=patient)



if __name__ == '__main__':
    app.run(debug = True)