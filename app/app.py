from flask import Flask, render_template, request
from waitress import serve
import fitz

from util import get_document_headers, get_headers_2
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

        F = open("file.pdf", "wb")
        F.write(f.read())
        doc = fitz.open("file.pdf")

        headers = get_document_headers(doc) + get_headers_2("file.pdf")
        headers = list(filter(lambda x: len(x) < 90 and len(x) > 4, headers))
        headers = list(set(headers))

        predictions = predict(headers)

        return render_template('result.html', headers=headers, predictions=predictions)

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
    # app.run(debug=True)
