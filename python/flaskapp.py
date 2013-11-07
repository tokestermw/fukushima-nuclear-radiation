from flask import Flask, request, render_template, json, jsonify

from interpolate import interpolate

import sys, logging
logging.basicConfig(stream = sys.stderr)

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def query():
    return render_template('/query.html')

@app.route("/query", methods = ['POST'])
def get_weightedLoc():
    data = json.loads(request.form.get('data'))
    #json.dump(data, 'data.json')
    print data
    return jsonify(data)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
