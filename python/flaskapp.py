from flask import Flask, request, render_template, json, jsonify

import numpy as np
from interpolate import interpolate, cv

import sys, logging
logging.basicConfig(stream = sys.stderr)

import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def query():
    return render_template('/query.html')

@app.route("/query", methods = ['POST'])
def get_weightedLoc():
    data = json.loads(request.form.get('data'))
    # with open('dump.json', 'w') as outfile:
    #     json.dump(data, outfile)

    global DATA
    DATA = data

    # set data
    # lat = np.array([i[1] for i in data])
    # lon = np.array([i[2] for i in data])
    # val = np.array([i[0] for i in data])

    # global GRID_RANGE
    # GRID_RANGE = {'lat': [min(lat), max(lat)], 'lon': [min(lon), max(lon)]}

    #smooth = interpolate(lat, lon, val)
    #smooth.set_grid(200, 50)
    #smooth.rbf()

    #global OUTPUT
    #OUTPUT = smooth.convert_gmaps2json()
    # with open('dumpS.json', 'w') as outfile:
    #     json.dump(OUTPUT, outfile)

    # jsonify(out = out)
    return 'Im not using this data in Javascript (client-side) for now'

@app.route("/sign", methods = ['POST'])
def calc_significance():
    data = json.loads(request.form.get('data'))

    lat = np.array([i[1] for i in DATA])
    lon = np.array([i[2] for i in DATA])
    val = np.log(np.array([i[0] for i in DATA]))

    smooth = interpolate(lat, lon, val)

    x = np.array([i[1] for i in data])
    y = np.array([i[2] for i in data])
    # cpm to microsievert to nanogray per hour
    z = np.log(np.array([i[0] for i in data]) / 350.0 * 1000.0)

    smooth.pick_points(x, y)

    choice = json.loads(request.form.get('choice'))

    s2_k = np.zeros(len(x))
    if choice == "Inverse Distance Weighting":
        smooth.simple_idw()
    elif choice == "Radial Basis Function":
        smooth.rbf()
    elif choice == "Ordinary Kriging":
        smooth.kriging()
        s2_k = np.sqrt(smooth.s2_k) * 1.96 # 95% CI

    z_smooth = smooth.z

    ## run cross validation
    cv_results = cv(choice, lat, lon, val)

    #    with open('dump2.json', 'w') as outfile:
    #    json.dump(data, outfile)
    return jsonify(result = (z / z_smooth).tolist(),
                   cv_results = cv_results,
                   z = z.tolist(),
                   z_smooth = z_smooth.tolist(),
                   s2_k = s2_k.tolist())

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
