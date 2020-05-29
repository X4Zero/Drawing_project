from flask import Flask
from flask import jsonify, json
from flask import request,render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)