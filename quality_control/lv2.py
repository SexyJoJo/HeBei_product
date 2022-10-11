import os.path
import pandas as pd
from datetime import datetime

def lv2_qc(station, element_num, time, elements83):
    """
    质控lv2的一条数据
    @param station: 站号
    @param element_num: 要素编号(11或13)
    @param time: 时间
    @param elements83: 83层高度的要素值列表
    @return: 质控码（0或1）， 1代表通过， 0代表不通过
    """
    station = str(station)
    element_num = str(element_num)
    time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    month = "0" + str(time.month) if len(str(time.month)) == 1 else str(time.month)
    config_path = os.path.join("./thresholds", station, f"EC统计数据_{station}_{month}.csv")
    df = pd.read_csv(config_path)

    if element_num == "11":
        max_ele = df["max_tem"].tolist()
        min_ele = df["min_tem"].tolist()
    elif element_num == "13":
        max_ele = df["max_rhu"].tolist()
        min_ele = df["min_rhu"].tolist()
    else:
        print("元素输入有误")
        return

    for i, element_value in enumerate(elements83):
        if min_ele[i] <= element_value <= max_ele[i]:
            continue
        else:
            return 0

    return 1


if __name__ == '__main__':
    values = [9.700, 9.616, 9.532, 9.448, 9.364, 9.226, 9.088, 8.950, 8.812, 8.659, 8.506, 8.353, 8.200, 8.016, 7.833, 7.649, 7.465, 7.307, 7.150, 6.992, 6.835, 6.524, 6.213, 5.896, 5.580, 5.301, 5.023, 4.770, 4.518, 4.261, 4.004, 3.782, 3.560, 3.332, 3.105, 2.909, 2.713, 2.542, 2.371, 2.141, 1.912, 1.792, 1.673, 1.477, 1.280, 1.067, 0.854, 0.680, 0.507, 0.267, 0.027, -1.088, -2.416, -3.695, -5.135, -6.439, -7.801, -9.207, -10.591, -12.253, -13.904, -15.425, -17.159, -18.704, -20.475, -22.171, -24.046, -25.891, -27.690, -29.571, -31.396, -33.407, -35.219, -37.193, -39.037, -41.045, -42.901, -44.847, -46.686, -48.451, -49.953, -51.452, -52.917]
    flag = lv2_qc(53996, 11, "2017-11-05 00:00:01", values)
    print(flag)