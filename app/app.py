from flask import Flask, render_template, request
from waitress import serve
import fitz

from util import get_document_headers, get_headers_2
from predict import predict


def is_filter_number(headers):
    headers_starting_with_digits = 0
    for header in headers:
        if len(header) >= 5 and header[0].isdigit():
            headers_starting_with_digits += 1
    return headers_starting_with_digits >= 5

def filter_numbers(headers):
    if is_filter_number(headers): 
        return list(filter(lambda header: header[0].isdigit(), headers))
    return headers

def is_filter_od_list(headers):
    headers_starting_with_digits = 0
    for header in headers:
        if len(header) >= 5 and header[1] == '.':
            headers_starting_with_digits += 1
    return headers_starting_with_digits >= 5

def filter_ordered_list_letters(headers):
    if is_filter_od_list(headers):
        return list(filter(lambda header: len(header) >= 2 and header[1] == '.', headers))
    return headers

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

        headers = filter_numbers(get_document_headers(doc))
        headers_bold = filter_ordered_list_letters(get_headers_2("file.pdf"))
        print(headers_bold)

        if is_filter_number(headers_bold) or is_filter_od_list(headers_bold):
            headers = headers_bold
        elif len(headers) <=8 :
            headers += headers_bold

        headers = list(filter(lambda x: len(x) < 90 and len(x) > 4, headers))

        headers = list(set(headers))

        predictions = predict(headers)

        return render_template('result.html', headers=headers, predictions=predictions)

if __name__ == "__main__":
    # serve(app, host='0.0.0.0', port=5000)
    app.run(debug=True)