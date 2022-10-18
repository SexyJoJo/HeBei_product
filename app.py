import base64
import json

import VWS
import parse_utils
from io import BytesIO
from flask import Flask, request, jsonify
import indices
import inversion_intensity
import TlnP
from pblh import get_pblh2
from VI import get_VI
from vorticity_divergence import get_divergence, get_vorticity

app = Flask(__name__)


@app.route('/')
@app.route('/inversionIntensity', methods=['POST'])
def inversionIntensity():
    data = json.loads(request.data)
    heights = data["heights"]
    temperatures = data["temperatures"]
    try:
        IOI, avgIOI = inversion_intensity.get_IOI(heights, temperatures)
        return jsonify({"result": IOI, "avgIOI": avgIOI, "msg": "success"})
    except Exception:
        return jsonify({"result": None, "msg": "fail"})


@app.route('/tlnp', methods=['POST'])
def tlnp():
    data = json.loads(request.data)
    tem = data["tem"]
    prs = data["prs"]
    rhu = data["rhu"]
    wind_speed = data["w_speed"]
    wind_direct = data["w_direct"]
    try:
        figdata = BytesIO()
        img = TlnP.plot_tlnp(tem, prs, rhu, wind_speed, wind_direct)
        img.savefig(figdata, format='jpg')

        figdata.seek(0)
        img_data = figdata.read()
        img_base64 = str(base64.b64encode(img_data))
        return jsonify({"img_base64": img_base64, "msg": "success"})

    except Exception as e:
        print(e)
        return jsonify({"img_base64": None, "msg": "fail"})


@app.route('/pblh', methods=['POST'])
def pblh():
    data = json.loads(request.data)
    heights = data["heights"]
    temperatures = data["temperatures"]
    try:
        PBLH = get_pblh2(heights, temperatures)
        return jsonify({"result": PBLH, "msg": "success"})
    except Exception as e:
        print(e)
        return jsonify({"result": None, "msg": "fail"})


@app.route('/VI', methods=['POST'])
def VI():
    data = json.loads(request.data)
    heights = data["heights"]
    temperatures = data["temperatures"]
    wind_speeds = data["w_speeds"]
    try:
        vi = get_VI(heights, temperatures, wind_speeds)
        return jsonify({"result": vi, "msg": "success"})
    except Exception as e:
        print(e)
        return jsonify({"result": None, "msg": "fail"})


@app.route('/divergence', methods=['POST'])
def divergence():
    data = json.loads(request.data)
    site1 = eval(data["site1"])
    site2 = eval(data["site2"])
    site3 = eval(data["site3"])
    try:
        result = get_divergence(site1, site2, site3)[0]
        return jsonify({"result": result, "msg": "success"})
    except Exception as e:
        print(e)
        return jsonify({"result": None, "msg": "fail"})


@app.route('/vorticity', methods=['POST'])
def vorticity():
    data = json.loads(request.data)
    site1 = eval(data["site1"])
    site2 = eval(data["site2"])
    site3 = eval(data["site3"])
    try:
        result = get_vorticity(site1, site2, site3)[0]
        return jsonify({"result": result, "msg": "success"})
    except Exception as e:
        print(e)
        return jsonify({"result": None, "msg": "fail"})


@app.route('/vws', methods=['POST'])
def vws():
    data = json.loads(request.data)
    tem = data["heights"]
    wind_speed = data["w_speeds"]
    wind_direct = data["w_directs"]
    try:
        figdata = BytesIO()
        img = VWS.plot_vws(tem, wind_speed, wind_direct)
        img.savefig(figdata, format='jpg')

        figdata.seek(0)
        img_data = figdata.read()
        img_base64 = str(base64.b64encode(img_data))
        return jsonify({"img_base64": img_base64, "msg": "success"})

    except Exception as e:
        print(e)
        return jsonify({"img_base64": None, "msg": "fail"})


@app.route('/utils/interp_tempers', methods=['POST'])
def interp_tempers():
    data = json.loads(request.data)
    height, data_heights, data_tempers = data["height"], data["data_heights"], data["data_tempers"]
    try:
        result = parse_utils.Lv2Utils.interp_tempers(height, data_heights, data_tempers)
        return jsonify({"result": result, "msg": "success"})
    except Exception as e:
        print(e)
        return jsonify({"result": None, "msg": "fail"})


@app.route('/utils/interp_wspeed', methods=['POST'])
def interp_wspeed():
    data = json.loads(request.data)
    height, data_heights, data_wspeeds = data["height"], data["data_heights"], data["data_wspeeds"]
    try:
        result = parse_utils.WindUtils.interp_wspeed(height, data_heights, data_wspeeds)
        return jsonify({"result": result, "msg": "success"})
    except Exception as e:
        print(e)
        return jsonify({"result": None, "msg": "fail"})


@app.route('/utils/interp_wdirect', methods=['POST'])
def interp_wdirect():
    data = json.loads(request.data)
    height, data_heights, data_wdirects = data["height"], data["data_heights"], data["data_wdirects"]
    try:
        result = parse_utils.WindUtils.interp_wspeed(height, data_heights, data_wdirects)
        return jsonify({"result": result, "msg": "success"})
    except Exception as e:
        print(e)
        return jsonify({"result": None, "msg": "fail"})


@app.route('/a_index', methods=['POST'])
def a_index():
    data = json.loads(request.data)
    pressure, temperature, humidity = data["prs"], data["tem"], data["rhu"]
    try:
        result = indices.A_index(pressure, temperature, humidity)
        return jsonify({"result": result, "msg": "success"})
    except Exception as e:
        print(e)
        return jsonify({"result": None, "msg": "fail"})


@app.route('/tt_index', methods=['POST'])
def tt_index():
    data = json.loads(request.data)
    pressure, temperature, rhu = data["prs"], data["tem"], data["rhu"]
    try:
        result = indices.TT_Index(pressure, temperature, rhu)
        return jsonify({"result": result, "msg": "success"})
    except Exception as e:
        print(e)
        return jsonify({"result": None, "msg": "fail"})


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0')
