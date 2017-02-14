from flask import Flask
import ocr

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello Gimp!'

@app.route('/ocr')
def do_ocr():
    image = 'static/bet2.jpg'
    ocr_obj = ocr.OCR(image)
    text = ocr_obj.ocr()
    return text


if __name__ == '__main__':
    app.run()
