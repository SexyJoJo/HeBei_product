import base64
import json
import TlnP
import parse_utils
import inversion_intensity
from io import BytesIO
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/inversionIntensity', methods=['POST'])
def inversionIntensity():
    data = json.loads(request.data)
    heights = data["heights"]
    temperatures = data["temperatures"]
    try:
        IOI = inversion_intensity.get_IOI(heights, temperatures)
        return jsonify({"result": IOI, "msg": "success"})
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


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0')
