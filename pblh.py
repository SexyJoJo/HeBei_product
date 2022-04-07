import pandas as pd
import numpy as np

def get_pblh(freq, bt):
    """
    计算边界层高度
    :param freq: 通道频率列表
    :param bt: 与freq相对应的亮温列表
    :return: 边界层高度
    """
    freq = np.array(freq)
    if len(freq) != len(bt):
        ex = Exception('频率和亮温数量不匹配')
        raise ex

    # col = [1, 8, 11, 17, 19, 22, 27, 28, 30, 33, 35, 38, 39, 41]
    col = np.array(
        [22.235, 23.835, 25.440, 30.000, 51.248, 51.5760, 53.340, 53.848, 53.860, 55.500, 56.660, 57.300, 57.960, 58.000]
    )
    # 多通道映射为14通道
    mapped_bt = []
    for i in col:
        temp = list(abs(freq-i))
        mapped_bt.append(bt[temp.index(min(temp))])
    print(mapped_bt)

    coe = np.array(
        [-24.69, 49.80, -123.93, 0, 40.14, 22.45, 95.61, -45.3, -29.95, 96.63, -252.47, -41.84, 1.54, 215.59]
    )
    b = 5497.46
    # try:
    #     df_lv1 = pd.read_csv(LV1_path, encoding="GBK", usecols=col)
    # except:
    #     df_lv1 = pd.read_csv(LV1_path, encoding="utf-8", usecols=col)
    pblh = np.dot(mapped_bt, coe) + b
    return pblh


if __name__ == '__main__':
    freqs = [22.234, 22.235, 22.240, 22.500, 23.034, 23.035, 23.040]
    bts = [1 for i in range(len(freqs))]
    print(get_pblh(freqs, bts))
