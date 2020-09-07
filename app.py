from flask import Flask, render_template , request, redirect



from werkzeug.utils import secure_filename

import os
import tensorflow
from tensorflow import keras
from keras.preprocessing.image import load_img,img_to_array,ImageDataGenerator


model = keras.models.load_model(".\my_model")

app = Flask(__name__)

def prediction(image_location,model):
	img = load_img(image_location,target_size=(150,150))
	img = img_to_array(img)/255.0
	img = img.reshape(1,150,150,3)
	pred = model.predict_proba(img)
	return pred
 
@app.route('/')
def hello():
	return render_template("index.html")

@app.route('/success',methods=['GET','POST'])
def success():
	if request.method == 'POST':  
		image_file = request.files["image"]
        # f.save(f.filename)  
		
		if(image_file):
			image_location = os.path.join(".\static",image_file.filename)
			image_file.save(image_location)
			pred = prediction(image_location,model)
			corona_prob = float(pred[0][0])
			normal_prob = float(pred[0][1])
			my_pred = ''
			if(corona_prob > normal_prob):
				my_pred = 'Positive'
			else:
				my_pred = 'Negative'
			return render_template("success.html", your_pred = my_pred)

		return render_template("success.html", your_pred='Invalid Input') 
if __name__ == '__main__':
	app.run(port=12000,debug=True)
