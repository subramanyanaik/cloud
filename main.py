 from flask import Flask

UPLOAD_FOLDER = r'C:\Users\smiles\Desktop\flaskfolder'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

import os
#import magic
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
labels = {0:'Actini keratoses', 1:'Basal cell carcinoma', 2:'Benign keratosis', 3:'dermatofibroma', 4:'melanoma', 5:'melanocytic nevi', 6:'Vascular lesions'}
#converting image to numpy array for processing
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
import numpy as np
import cv2
from keras.preprocessing import image
from keras.models import load_model
import matplotlib.pyplot as plt
classifier = load_model('prototype4.h5')
import os      
labels = {0:'Actini keratoses', 1:'Basal cell carcinoma', 2:'Benign keratosis', 3:'dermatofibroma', 4:'melanoma', 5:'melanocytic nevi', 6:'Vascular lesions'}

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			img = plt.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			import numpy as np
			import cv2
			from keras.preprocessing import image
			from keras.models import load_model
			classifier = load_model('prototype4.h5')
			img = cv2.resize(img, (100, 75))
			test_image = image.img_to_array(img)
			test_image = np.expand_dims(test_image, axis=0)
			# image normalisation to reduce the range of pixel values
			test_image = test_image / 255
			print(np.shape(test_image))
			result = classifier.predict(test_image)
			disease_detected = labels[np.argmax(result[0], axis=0)]
			print(disease_detected)
			flash(disease_detected)
			return redirect('/')
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return redirect(request.url)

if __name__ == "__main__":

    app.run(port=5000)