from flask import Flask,render_template,request,redirect
from tensorflow.keras.preprocessing.image import load_img,img_to_array
import pickle
import numpy as np
from tensorflow.keras.models import load_model



app = Flask(__name__)

model = load_model('model.h5')

@app.route('/')
def home():
    return render_template('home.html')

import os
@app.route('/predictor' , methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        file = request.files["filename"]
        filename = file.filename
        file_path = os.path.join('static/uploads',filename)
        file.save(file_path)

        test_img = load_img(file_path,target_size=(150,150))
        test_img = img_to_array(test_img)
        test_img = np.expand_dims(test_img,axis=0)
        res = model.predict(test_img)
        
        pred = np.argmax(res)
        
        if pred == 0:
            op = "This Picture Represent Diseased Cotton leaf"

        if pred == 1:
            op = "This Picture Represent Diseased Cotton plant"

        if pred == 2:
            op = "This Picture Represent Fresh Cotton leaf"

        if pred == 3:
            op = "This Picture Represent Fresh Cotton plant"


        return render_template('output.html',img_path = file_path,op=op)
    return render_template('predict.html')




if __name__ == '__main__':
    app.run(debug=True)

    