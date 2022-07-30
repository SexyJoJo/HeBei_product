import math
from parse_utils import *
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
        G = 9.8     # 重力加速度
        Rc = 0.25
        h0 = 0
        h = h0
        t0 = get_temp(h, heights, temperatures)
        p0 = get_prs(h, heights, pressures)
        potem0 = get_potem(t0, p0)  # 计算位温
        # 获取不同高度下的要素值
        # Ris = []
        while True:
            # 获取当前高度对应的气象要素
            t = get_temp(h, heights, temperatures)
            p = get_prs(h, heights, pressures)
            potem = get_potem(t, p)     # 位温
            w_speed = get_wspeed(h, heights, w_speeds)
            w_direct = get_wdirect(h, heights, w_directs)
            u = w_speed * math.sin(w_direct)    # 纬向风分量
            v = w_speed * math.cos(w_direct)    # 经向风分量

            Ri = (G * (h - h0) / potem) * ((potem - potem0) / (u**2 + v**2))
            # Ris.append(round(Ri, 3))

            print(Ri)
            # 首次Ri／Rc＞１的高度作为边界层高度
            if Ri / Rc > 1:
                # h += 50
                return h
            else:
                h0 = h
                potem0 = potem
                h += 100
            # print(Ris)
    except Exception as e:
        print(e)


def get_pblh2(heights, temperatures):
    """
    探空数据位温法计算边界层高度
    @param heights: 高度列表
    @param temperatures: 温度列表
    @return: 边界层高度
    """
    # sounding_df = SoundingUtils.cap_by_height(sounding_df, 2000)
    # heights = sounding_df["GPH"].tolist()
    # temperatures = sounding_df["TEM"].tolist()

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
    # 方法二
    for root, _, files in os.walk(r"Lv2数据"):
        for file in files:
            if file.endswith("CP_M.txt"):
                fullpath = os.path.join(root, file)
                tempers, heights = Lv2Utils.get_tem_M(fullpath)
                print(f"时间：{Lv2Utils.get_time(file)}  边界层高度：{get_pblh2(heights, tempers)}")

    # 方法三
    tempers = [-7.8, -7.33, -6.68, -5.91, -5.29, -4.86, -4.41, -3.97, -3.61, -3.35, -2.98, -2.66, -2.47, -2.24, -2.03, -1.88, -1.82, -1.77, -1.71, -1.62, -1.66, -1.73, -1.88, -2.05, -2.36, -2.65, -2.86, -3.14, -3.53, -3.86, -4.18, -4.57, -4.97, -5.37, -5.75, -6.12, -6.45, -6.7, -6.95, -7.21, -7.49, -7.77, -8.09, -8.36, -8.67, -8.95, -9.22, -9.5, -9.86, -10.25, -10.86, -11.7, -12.64, -13.72, -14.87, -16.05, -17.14, -18.4, -19.81, -21.33, -22.92, -24.71, -26.55, -28.5, -30.44, -32.33, -34.24, -36.19, -38.02, -39.82, -41.73, -43.58, -45.33, -47.14, -49.09, -50.88, -52.58, -54.2, -55.57, -56.77, -57.7, -58.36, -58.77]
    _, heights = Lv2Utils.get_tem_D(r"D:\Data\河北产品\LV2\54511-AD-2021-01-01LV2-QC.csv")
    pressures = MetCals.bat_height2prs(heights)
    wind_df = ParseFiles.parse_minute_wind(r"D:\Data\河北产品\分钟级风廓线\南郊风廓线\01\Z_RADA_54511_WPRD_MOC_NWQC_HOBS_LC_QI_20210101000000.TXT""")
    ori_heights = wind_df["height"].tolist()
    print("风阔线高度：", ori_heights)
    ori_directs = wind_df["hori_direct"].tolist()
    ori_speeds = wind_df["hori_speed"].tolist()
    directs, speeds = [], []
    for h in heights:
        directs.append(WindUtils.interp_wdirect(h, ori_heights, ori_directs))
        speeds.append(WindUtils.interp_wspeed(h, ori_heights, ori_speeds))
    pblh = get_pblh(heights, tempers, pressures, speeds, directs)
    print("高度：", heights)
    print("温度：", tempers)
    print("压强：", pressures)
    print("风速：", speeds)
    print("风向：", directs)
    print("边界层高度", pblh)
