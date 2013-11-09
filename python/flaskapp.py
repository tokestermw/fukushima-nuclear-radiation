from flask import Flask, request, render_template, json, jsonify

import numpy as np
from interpolate import interpolate

import sys, logging
logging.basicConfig(stream = sys.stderr)

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def query():
    global OUTPUT
    OUTPUT = []
    return render_template('/query.html')

@app.route("/query", methods = ['POST'])
def get_weightedLoc():
    data = json.loads(request.form.get('data'))
    # with open('dump.json', 'w') as outfile:
    #     json.dump(data, outfile)

    # set data
    lat = np.array([i['location']['nb'] for i in data])
    lon = np.array([i['location']['ob'] for i in data])
    val = np.array([i['weight'] for i in data])

    smooth = interpolate(lat, lon, val)
    smooth.set_area(200, 50)
    smooth.rbf()

    OUTPUT = smooth.convert_gmaps2json()

    # jsonify(out = out)
    return 'I just pass it within Flask since Im not using this data in Javascript for now'

@app.route("/sign", methods = ['POST'])
def calc_significance():
    data = json.loads(request.form.get('data'))
    print data
    return jsonify(result = 1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
