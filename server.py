<<<<<<< HEAD
from flask import Flask
import ocr
=======
import os, ocr
from flask import Flask, jsonify
>>>>>>> 7349cb9d052082289bdc92897481da346d23355d

app = Flask(__name__)

@app.route('/')
<<<<<<< HEAD
def hello_world():
    return 'Hello Gimp!'

@app.route('/ocr')
def do_ocr():
    image = 'static/bet2.jpg'
=======
def welcome():
    return app.send_static_file('index.html')

@app.route('/ocr')
def do_ocr():
    image = 'static/images/bet2.jpg'
>>>>>>> 7349cb9d052082289bdc92897481da346d23355d
    ocr_obj = ocr.OCR(image)
    text = ocr_obj.ocr()
    return text

<<<<<<< HEAD

if __name__ == '__main__':
    app.run()
=======
port = os.getenv('PORT', '8080')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
>>>>>>> 7349cb9d052082289bdc92897481da346d23355d
