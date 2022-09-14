import math
import os

import vorticity_divergence
from parse_utils import *

heights = [150, 270, 390, 510, 630, 750, 870, 990, 1110, 1230, 1350, 1470, 1590, 1710, 1830, 1950]

for h in heights:
    stations = {}
    for root, dirs, files in os.walk("../风廓线数据/各站点同时刻风廓线"):
        for file in files:
            info = []

            station = file.split("_")[3]

            file_path = os.path.join(root, file)
            df = ParseFiles.parse_minute_wind(file_path)
            lon, lat = WindUtils.get_site(file_path)

            w_speed = df[df["height"] == h]["hori_speed"].tolist()[0]
            w_direct = df[df["height"] == h]["hori_direct"].tolist()[0]
            u = round(w_speed * math.sin(w_direct), 2)  # 纬向风分量
            v = round(w_speed * math.cos(w_direct), 2)  # 经向风分量

            # info.append()
            stations[station] = (lon, lat, u, v)

    # print(stations)
    # diver = vorticity_divergence.get_divergence(stations["53399"], stations["53996"], stations["54304"])
    # vorti = vorticity_divergence.get_vorticity(stations["53399"], stations["53996"], stations["54304"])
    # print(f"站点53399, 53996, 54304")
    # print(f"高度层{h}：涡度：{vorti[0]}, 散度：{diver[0]}")

    diver = vorticity_divergence.get_divergence(stations["54311"], stations["54534"], stations["54304"])
    vorti = vorticity_divergence.get_vorticity(stations["54311"], stations["54534"], stations["54304"])
    print(f"站点54311, 54534, 54304")
    print(f"高度层{h}：涡度：{vorti[0]}, 散度：{diver[0]}")
