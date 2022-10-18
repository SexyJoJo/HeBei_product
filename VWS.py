"""绘制垂直风切图"""
import math

import matplotlib.pyplot as plt
import numpy as np
from parse_utils import WindUtils


def get_u(speed, direct):
    return round(speed * math.sin(direct), 3)


def get_v(speed, direct):
    return round(speed * math.cos(direct), 3)


def cal_vws(u1, u2, v1, v2, h1, h2):
    vws = math.sqrt(pow(u1 - u2, 2) + pow(v1 - v2, 2)) / (h1 - h2) * 1000
    return round(vws, 3)


def plot_vws(heights, w_speeds, w_directs):
    new_heights, us, vs = [], [], []

    # 插值获取均匀高度层数据
    for h in range(0, 3000, 125):
        wspeed = WindUtils.interp_wspeed(h, heights, w_speeds)
        wdirect = WindUtils.interp_wdirect(h, heights, w_directs)
        u = get_u(wspeed, wdirect)
        v = get_v(wspeed, wdirect)
        new_heights.append(h)
        us.append(u)
        vs.append(v)

    x = np.zeros((24, 24))
    for k, h1 in enumerate(new_heights[::-1]):  # h1>h2
        for j, h2 in enumerate(new_heights):
            i = -(k+1)
            try:
                vws = cal_vws(us[j], us[i], vs[j], vs[i], h1, h2)
                print(i, j, h1, h2, vws)
            except ZeroDivisionError:
                vws = np.nan

            if h2 >= h1:
                vws = np.nan

            x[23-j][23-k] = vws

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.imshow(x, cmap="plasma")
    plt.colorbar()
    plt.xticks(np.arange(0, 24, 2), np.arange(0, 3, 6/24))
    plt.yticks(np.arange(0, 24, 2), np.arange(3, 0, -6/24))
    plt.xlabel("顶高 km")
    plt.ylabel("底高 km")
    plt.title("垂直风切变 m/(s·km)")
    # plt.show()
    return plt

