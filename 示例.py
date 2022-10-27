import os

import pandas as pd

import parse_utils
import TlnP
import pblh
import VI
import inversion_intensity
import VWS

# 高度数组，单位：m
height = [120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 840, 960, 1080, 1200, 1320, 1440, 1560, 1680, 1800, 1920, 2040, 2160, 2280]
# 温度数组，单位：℃
tem = [14.155, 14.116, 14.195, 14.332, 14.331, 14.276, 14.115, 13.955, 13.797, 13.541, 12.645, 11.79, 10.963, 10.0, 9.29, 8.393, 7.534, 6.793, 6.058, 5.431, 4.736, 4.075, 3.416]
# 气压数组， 单位：hPa
prs = [998.92, 991.817, 984.754, 977.733, 970.752, 963.811, 956.911, 950.051, 943.23, 936.45, 916.344, 903.135, 890.082, 877.181, 864.432, 851.834, 839.384, 827.083, 814.927, 802.917, 791.051, 779.327, 767.744]
# 风速数组， 单位：m/s
w_speed = [1.4, 2.1, 3.5, 4.0, 4.0, 6.9, 9.8, 11.4, 10.6, 7.8, 12.2, 12.5, 13.7, 14.9, 15.0, 14.6, 14.8, 17.7, 15.3, 14.6, 14.2, 14.0, 14.5]
# 风向数组， 单位：°
w_direct = [205.0, 289.4, 314.1, 312.4, 265.6, 249.3, 244.4, 247.7, 245.9, 251.7, 204.5, 203.8, 205.1, 198.7, 187.1, 182.9, 190.8, 213.0, 192.9, 155.8, 145.5, 146.5, 159.6]
# 相对湿度数组， 单位：%
rhu = [26.26, 12.07, 7.38, 7.65, 8.81, 10.07, 9.83, 9.93, 10.58, 12.51, 14.45, 15.07, 14.14, 13.55, 13.79, 17.48, 21.28, 19.33, 19.65, 19.52, 24.43, 24.43, 24.43]

# 绘制TlnP图, 返回图片对象
# plt = TlnP.plot_tlnp(tem, prs, rhu, w_speed, w_direct)
# plt.show()

# plt = VWS.plot_vws(height, w_speed, w_direct)
# plt.show()

# for root, dirs, files in os.walk("Lv2数据"):
#     for file in files:
#         if file.endswith('CP_M.txt'):
#             # print(file)
#             tem, height = parse_utils.Lv2Utils.get_tem_M(os.path.join(root, file))
#             # print(tem)
#             # print(height)
#             # 计算逆温强度（若存在逆温层，则返回二维数组，每个一维数组对应一个逆温层）
#             # [[底高1， 顶高1，逆温强度1], [底高2， 顶高2，逆温强度2], ... ](可能出现多个逆温层)
#             # IOI_result = inversion_intensity.get_IOI(height, tem)
#             # # 计算边界层高度
#             # pblh_result = pblh.get_pblh2(height, tem)
#             # # 计算边界层通风量
#             VI_result = VI.get_VI(height, tem, w_speed)

            # if not IOI_result == []:
            #     print(IOI_result)
            # print(pblh_result)
            # print(VI_result)



# plt.show()

parse_utils.Lv1Utils.brt2lv1(58424, r"C:\Users\JOJO\Desktop\安庆LV1", r"C:\Users\JOJO\Desktop\安庆_LV1")
