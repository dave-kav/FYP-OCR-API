from flask import Flask
import os, ocr
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello!'

@app.route('/welcome')
def welcome():
    return app.send_static_file('index.html')

@app.route('/ocr')
def do_ocr():
    image = 'static/images/bet2.jpg'
    ocr_obj = ocr.OCR(image)
    text = ocr_obj.ocr()
    return text

port = os.getenv('PORT', '8080')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))

