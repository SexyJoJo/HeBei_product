import matplotlib.pyplot as plt
from inversion_intensity import get_IOI
import os
import pandas as pd
from pblh import get_pblh
from VI import get_VI
import numpy as np


def read_file(file):
    """读取目录中lv2文件"""
    print(f"正在处理{file}")
    cp_df = pd.read_csv(file, encoding='gbk', skiprows=2)
    t_df = cp_df[cp_df['10'] == 11].set_index('Record')
    # 去除无用列
    t_df = t_df.drop(columns=["10", "SurTem(℃)", "SurHum(%)", "SurPre(hPa)",
                              "Rain", "Tir(℃)", "QCflag", "CloudBase(km)", "Vint(mm)", "Lqint(mm)"])
    # 去除表头中的单位
    new_cols = []
    for col in t_df.columns:
        if col.endswith('(km)'):
            new_cols.append(col[:-4])
        else:
            new_cols.append(col)
    t_df.columns = new_cols

    t_df['IOI'] = None
    return t_df


# for root, _, files in os.walk(r"D:\Data\microwave radiometer\Measured brightness temperature\54510廊坊"):
#     for file in files:
#         if file.endswith("CP_D.txt"):
#             df = read_file(os.path.join(root, file))
#             for i, row in df.iloc[:, 1:-1].iterrows():
#                 ioi = get_IOI(row.index, row.values)
#                 print(ioi)

# heights = [150, 270, 390, 510, 630, 750, 870, 990, 1110, 1230, 1350, 1470, 1590, 1710, 1830, 1950, 2070, 2190, 2310,
#            2430, 2550, 2670, 2790, 2910, 3030, 3150, 3270, 3390, 3630, 3870, 4110, 4350, 4590, 4830, 5070, 5310, 5550,
#            5790, 6030]
#
# directs = [284.8, 290.9, 299.7, 308.4, 331.7, 332.3, 331.9, 330.9, 329.5, 327.6, 325.0, 321.5, 317.4, 312.9, 308.8,
#            305.0, 300.3, 293.6, 285.6, 278.7, 274.6, 272.6, 271.7, 271.5, 272.6, 274.1, 275.5, 276.1, 276.2, 276.7,
#            277.3, 277.9, 278.1, 278.1, 278.1, 279.2, 280.7, 281.3, 280.1]
#
# speeds = [3.6, 4.1, 5.4, 7.3, 14.2, 16.5, 18.2, 19.1, 20.3, 21.7, 23.0, 23.4, 23.7, 24.4, 25.5, 26.2, 26.3, 26.1, 26.2,
#           26.7, 27.3, 27.6, 27.5, 27.8, 28.2, 29.4, 30.7, 31.2, 31.6, 32.1, 33.7, 35.3, 36.4, 37.1, 37.5, 37.9, 38.2,
#           38.3, 38.1]
#
# pressures = [995.363, 981.238, 967.276, 953.476, 939.835, 926.353, 913.027, 899.858, 886.842, 873.98, 861.268, 848.707,
#              836.295, 824.03, 811.911, 799.937, 788.107, 776.418, 764.87, 753.462, 742.191, 731.058, 720.06, 709.197,
#              698.467, 687.868, 677.4, 667.062, 646.768, 626.977, 607.679, 588.865, 570.525, 552.651, 535.233, 518.262,
#              501.729, 485.626, 469.944]
#
# temperatures = [15, 14.5, 14.0, 13.5, 13.0, 12.5, 12.0, 11.5, 11.0, 10.5, 10.0, 9.5, 9.0, 8.5, 8.0, 7.5, 7.0, 6.5, 6.0,
#                 5.5, 5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5, 0.0, -0.5, -1.0, -1.5, -2.0, -2.5, -3.0, -3.5,
#                 -4.0]

# df = pd.read_table(r"D:\Data\风廓线\Z_RADA_I_53399_20220425203000_P_WPRD_LC_ROBS.TXT", skiprows=3, sep=r'\s+',
#                    names=['height', 'direct', 'h_speed', 'v_speed', 'h_credi', 'v_credi', 'Cn2'])
# df = df.iloc[:39, :]
# df['height'] = df['height'].astype(int)
# df['direct'] = df['direct'].astype(float)
# df['h_speed'] = df['h_speed'].astype(float)
# df['v_speed'] = df['v_speed'].astype(float)
#
# print(df)

# pblh = get_pblh(heights, temperatures, pressures, speeds, directs)
# print(pblh)
#
# VI = get_VI(heights, temperatures, pressures, speeds, directs)
# print(VI)

tDiffList = [4.159, 7.492, -2.963, 2.923, 1.365, 1.379, 2.49, 6.356, 10.696, 4.227, 11.514, 6.835, 8.658, 8.988, 146.732, 5.592, 2.439, 1.331, 4.194, 5.514, 0.003, 5.018, -0.149, 5.277, 0.602, 7.917, 6.381, 10.476, 2.317, 8.691, 1.295, 43.783, 15.86, 6.442, 6.634, 6.361, 11.062, 1.22, 13.95, 12.05, 45.598, 106.51, 33.57, 2.004, 8.614, 3.748, 4.122, 7.598, 1.704, 1.741, 6.096, 1.803, 4.55, 4.776, 4.81, 1.143, 3.429, 1.12, 3.602, 5.044, 3.466, 6.68, 6.734, 1.265, 2.62, 4.484, 3.634, 7.239, 5.398, 4.795, 3.513, 5.886, 3.02, 3.196, 9.813, 10.581]
tLiquidList = [32.454, 32.307, 29.718, 27.795, 23.074, 26.387, 25.949, 25.456, 27.139, 29.263, 29.46, 34.617, 29.262, 29.024, 244.174, 22.878, 27.422, 22.474, 21.688, 27.868, 31.038, 30.78, 34.445, 32.685, 33.294, 36.351, 33.301, 44.563, 37.09, 34.407, 35.442, 108.116, 33.89, 47.359, 28.628, 25.986, 26.97, 29.204, 32.087, 33.798, 157.294, 211.995, 112.854, 30.481, 29.447, 30.862, 22.071, 25.042, 26.113, 35.153, 37.408, 34.847, 31.22, 28.6, 35.439, 21.284, 25.14, 19.951, 21.246, 26.582, 23.468, 22.016, 23.333, 26.392, 22.361, 20.778, 22.837, 29.253, 26.041, 25.736, 27.181, 27.984, 28.859, 26.536, 27.675, 28.68]


correction = np.polyfit(x=tDiffList,
                        y=tLiquidList,
                        deg=2)
z = np.polyval(correction, tDiffList)
# z = np.polyval(correction, tDiffList)
results = []
for i in tDiffList:
    a = i * i * correction[0] + i * correction[1] + correction[2]
    results.append(a)

plt.plot(tDiffList, tLiquidList, 'o')
print(correction)
plt.plot(tDiffList, z)
# plt.plot(tDiffList, results)
plt.show()