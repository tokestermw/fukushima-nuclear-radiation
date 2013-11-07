from flask import Flask, request, render_template, json, jsonify

import sys, logging
logging.basicConfig(stream = sys.stderr)

app = Flask(__name__)

# @app.route('/', methods = ['GET'])
# def home():
#     return render_template('/home.html')

# @app.route('/_temp')
# def get_data():
#     #data = json.loads(request.form.get('datepicker'))
#     #print data
#     return 'aho'

# @app.route("/", methods = ['POST'])
# def get_data():
#     data = json.loads(request.form.get('data'))
#     ss = data['value']
#     return jsonify(data)

@app.route('/', methods = ['GET'])
def query():
    return render_template('/query.html')

@app.route("/", methods = ['POST'])
def get_weightedLoc():
    data = json.loads(request.form.get('data'))
    print data
    return jsonify(data)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
