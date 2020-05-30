from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_restful import Api, Resource, reqparse
import requests
import subprocess
import json

app = Flask(__name__)
api = Api(app)
app.config['TESTING'] = True

class Classify(Resource):
    @classmethod
    def get(cls, url):
        r = requests.get(url)
        retJson = {}
        with open('temp.jpg', 'wb') as f:
            f.write(r.content)
            proc = subprocess.Popen('python classify_image.py --model_dir=. --image_file=./temp.jpg', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            ret = proc.communicate()[0]
            proc.wait()
            with open("text.txt") as f:
                retJson = json.load(f)

        return retJson

api.add_resource(Classify, '/classify/<path:url>')

@app.template_filter('two_point')
def to_point(num):
    return round(num * 100, 2)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        r = requests.get(f'http://localhost:5000/classify/{url}')
        return render_template("index.html", data={'info': r.json(), 'url': url})
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')
