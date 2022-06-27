import math
from 测试.parse_utils import *
import numpy as np

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
    try:
        G = 9.8
        Rc = 0.25
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
    except Exception as e:
        print(e)


def get_pblh2(sounding_df):
    """
    探空数据位温法计算边界层高度
    @param sounding_df:
    @return:
    """
    sounding_df = SoundingUtils.cap_by_height(sounding_df, 2000)
    heights = sounding_df["GPH"].tolist()
    temperatures = sounding_df["TEM"].tolist()

    h = heights[0]
    grids = []
    while h <= 2000:
        t = SoundingUtils.interp_tempers(h, heights, temperatures)
        p = MetCals.height2prs(h)
        # 第一次计算位温特殊处理
        if h == heights[0]:
            pre_potem = MetCals.get_potem(t, p)
            h += 20
            continue
        else:
            crr_potem = MetCals.get_potem(t, p)
            grid = (crr_potem - pre_potem) / 20
            grids.append(grid)
            # 推进循环
            pre_potem = crr_potem
            h += 20

    grids = np.array(grids)
    pblh = heights[0] + grids.argmax() * 20
    return int(pblh)


if __name__ == '__main__':
    for root, _, files in os.walk(r"D:\Data\microwave radiometer\Sounding\54510"):
        for file in files:
            if file.endswith("SURP.txt"):
                fullpath = os.path.join(root, file)
                df = ParseFiles.parse_sounding(fullpath)
                print(get_pblh2(df))

