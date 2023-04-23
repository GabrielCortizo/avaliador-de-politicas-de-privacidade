from flask import Flask, render_template, request
from waitress import serve
import fitz

from util import get_document_headers
from predict import predict

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")

@app.route("/about", methods=['GET'])
def about():
    return render_template("about.html")

@app.route("/criteria", methods=['GET'])
def criteria():
    return render_template("criteria.html")

@app.route("/privacy-policy", methods=['GET'])
def get_privacy_policy():
    return render_template("result.html")
	
@app.route('/privacy-policy', methods = ['POST'])
def post_privacy_policy():
        f = request.files['file']
        doc = fitz.open(stream=f.read(), filetype="pdf")

        headers = list(filter(lambda x: len(x) < 80, get_document_headers(doc)))

        predictions = predict(headers)

        return render_template('result.html', headers=headers, predictions=predictions)

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
    # app.run(debug=True)