import json
import TlnP
import os
import inversion_intensity
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/inversionIntensity', methods=['GET', 'POST'])
def inversionIntensity():
    data = json.loads(request.data)
    heights = data["heights"]
    temperatures = data["temperatures"]
    try:
        IOI = inversion_intensity.get_IOI(heights, temperatures)
        return jsonify({"result": IOI, "msg": "success"})
    except Exception:
        return jsonify({"result": None, "msg": "fail"})


@app.route('/tlnp', methods=['GET', 'POST'])
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
        return jsonify({"img_path": img_path, "msg": "success"})
    except Exception as e:
        print(e)
        return jsonify({"img_path": None, "msg": "fail"})


if __name__ == '__main__':
    app.run()
