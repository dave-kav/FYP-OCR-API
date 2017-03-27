import os, ocr
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
#disable csrf protection

CORS(app)

#increase max file upload limit
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

#enable ssl to serve over https
context = ('cert.crt','key.key')

@app.route('/ocr', methods=['GET', 'POST'])
def analyze_bet():
    if request.method == 'POST':
        if 'imgData' in request.values:
            ocr_obj = ocr.OCR(request.values['imgData'])
            data = ocr_obj.analyze_bet()
            print data
            return jsonify(ocr=data)
        else:
            data = {'time': '', 'track': '', 'selection': '', 'odds': ''}
            return jsonify(ocr=data)
    else:
        #dummy data for dev
        data = {'time': '14:35', 'track': 'Galway', 'selection': 'Kauto Star', 'odds': '21/20'}
        return jsonify(ocr=data)

@app.route('/ocr/stake', methods=['GET', 'POST'])
def identify_stake():
    if request.method == 'POST':
        if 'imgData' in request.values:
            ocr_obj = ocr.OCR(request.values['imgData'])
            data = ocr_obj.identify_stake()
            print data
            return jsonify(ocr=data)
        else:
            data = {'stake': ''}
            return jsonify(ocr=data)
    else:
        #dummy data for dev
        data = {'stake': '25.00'}
        return jsonify(ocr=data)

port = os.getenv('PORT', '8081')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))

