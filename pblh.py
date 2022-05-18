import pandas as pd
import numpy as np
import math
from scipy.interpolate import interp1d

# def get_pblh(freq, bt):
#     """
#     经验公式法计算边界层高度
#     :param freq: 通道频率列表
#     :param bt: 与freq相对应的亮温列表
#     :return: 边界层高度
#     """
#     freq = np.array(freq)
#     if len(freq) != len(bt):
#         ex = Exception('频率和亮温数量不匹配')
#         raise ex
#
#     # col = [1, 8, 11, 17, 19, 22, 27, 28, 30, 33, 35, 38, 39, 41]
#     col = np.array(
#         [22.235, 23.835, 25.440, 30.000, 51.248, 51.5760, 53.340, 53.848, 53.860, 55.500, 56.660, 57.300, 57.960, 58.000]
#     )
#     # 多通道映射为14通道
#     mapped_bt = []
#     for i in col:
#         temp = list(abs(freq-i))
#         mapped_bt.append(bt[temp.index(min(temp))])
#     print(mapped_bt)
#
#     coe = np.array(
#         [-24.69, 49.80, -123.93, 0, 40.14, 22.45, 95.61, -45.3, -29.95, 96.63, -252.47, -41.84, 1.54, 215.59]
#     )
#     b = 5497.46
#     # try:
#     #     df_lv1 = pd.read_csv(LV1_path, encoding="GBK", usecols=col)
#     # except:
#     #     df_lv1 = pd.read_csv(LV1_path, encoding="utf-8", usecols=col)
#     pblh = np.dot(mapped_bt, coe) + b
#     return pblh


def get_temp(height, data_height, data_temp):
    f = interp1d(data_height, data_temp, bounds_error=False, fill_value='extrapolate')
    return f(height)

def get_prs(height, data_height, data_prs):
    f = interp1d(data_height, data_prs, bounds_error=False, fill_value='extrapolate')
    return f(height)

def get_wspeed(height, data_height, data_wspeeds):
    f = interp1d(data_height, data_wspeeds, bounds_error=False, fill_value='extrapolate')
    if f(height) <= 0:
        return 0.1
    return f(height)

def get_wdirect(height, data_height, data_wdirect):
    try:
        for i in range(len(data_wdirect) - 1):
            if data_wdirect[i] > 270 and data_wdirect[i+1] < 90:
                i = i+1
                while data_wdirect[i] < 90:
                    data_wdirect[i] += 360
                    i += 1
            elif data_wdirect[i] < 90 and data_wdirect[i+1] > 270:
                j = i
                while data_wdirect[j] < 90:
                    data_wdirect[j] += 360
                    j -= 1
    except IndexError:
        pass
    f = interp1d(data_height, data_wdirect, bounds_error=False, fill_value='extrapolate')
    w_dircect = f(height)
    if w_dircect >= 360:
        w_dircect -= 360
    return w_dircect

def get_potem(t, p):
    """计算位温"""
    return (t + 273.15) * ((1000 / p) ** (2/7))

def get_pblh(heights, temperatures, pressures, w_speeds, w_directs):
    """
    总理查森数法计算边界层高度
    :param heights: 高度列表
    :param temperatures: 温度列表
    :param pressures: 压强列表
    :param w_speeds: 风速列表
    :param w_directs: 风向列表
    :return: 边界层高度
    """
    G = 9.8
    Rc = 0.21
    h0 = 0
    h = h0
    t0 = get_temp(h, heights, temperatures)
    p0 = get_prs(h, heights, pressures)
    potem0 = get_potem(t0, p0)
    # 获取不同高度下的要素值
    while True:
        t = get_temp(h, heights, temperatures)
        p = get_prs(h, heights, pressures)
        potem = get_potem(t, p)     # 位温
        w_speed = get_wspeed(h, heights, w_speeds)
        w_direct = get_wdirect(h, heights, w_directs)
        u = w_speed * math.sin(w_direct)    # 纬向风分量
        v = w_speed * math.cos(w_direct)    # 经向风分量
        Ri = (G * (h - h0) / potem) * ((potem - potem0) / (u**2 + v**2))

        if Ri / Rc > 1:
            return h
        else:
            h += 1
