import base64
import json
import TlnP
import os
import inversion_intensity
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
        img = TlnP.plot_tlnp(tem, prs, rhu, wind_speed, wind_direct)
        img.savefig("tlnp.jpg")
        img_path = os.path.join(os.getcwd(), "tlnp.jpg")
        with open(img_path, 'rb') as f:
            img = str(base64.b64encode(f.read()))
            return jsonify({"img_base64": img, "msg": "success"})
    except Exception as e:
        print(e)
        return jsonify({"img_base64": None, "msg": "fail"})


if __name__ == '__main__':
    app.run()
