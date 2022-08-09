import os
from datetime import timedelta

import matplotlib.pyplot as plt

import pblh
import VI
from parse_utils import *


# if __name__ == '__main__':
# ParseFiles.cap_week_wind("daatt", "54510", "2022-05-08 16:00:00")
# height, w_speed, w_direct = get_height_speed_direct(r"./Data/wind_54510_22050216.txt")
# tem_83, HEIGHT_83 = get_tem_M(r"D:\Data\河北产品\微波辐射计\Z_UPAR_I_54510_20220502160000_P_YMWR_6000A_CP_M.txt")
# height, w_speed, w_direct = get_height_speed_direct(r"./Data/wind_54510_22050316.txt")
# tem_83, HEIGHT_83 = get_tem_M(r"D:\Data\河北产品\微波辐射计\Z_UPAR_I_54510_20220503160000_P_YMWR_6000A_CP_M.txt")
# height, w_speed, w_direct = get_height_speed_direct(r"./Data/wind_54510_22050416.txt")
# tem_83, HEIGHT_83 = get_tem_M(r"D:\Data\河北产品\微波辐射计\Z_UPAR_I_54510_20220504160000_P_YMWR_6000A_CP_M.txt")
# height, w_speed, w_direct = get_height_speed_direct(r"./Data/wind_54510_22050516.txt")
# tem_83, HEIGHT_83 = get_tem_M(r"D:\Data\河北产品\微波辐射计\Z_UPAR_I_54510_20220505160000_P_YMWR_6000A_CP_M.txt")
# height, w_speed, w_direct = get_height_speed_direct(r"./Data/wind_54510_22050616.txt")
# tem_83, HEIGHT_83 = get_tem_M(r"D:\Data\河北产品\微波辐射计\Z_UPAR_I_54510_20220506160000_P_YMWR_6000A_CP_M.txt")
# height, w_speed, w_direct = get_height_speed_direct(r"./Data/wind_54510_22050716.txt")
# tem_83, HEIGHT_83 = get_tem_M(r"D:\Data\河北产品\微波辐射计\Z_UPAR_I_54510_20220507160000_P_YMWR_6000A_CP_M.txt")
# height, w_speed, w_direct = ParseUtils.get_height_speed_direct(r"./Data/wind_54510_22050816.txt")
# tem_83, HEIGHT_83 = ParseUtils.get_tem_M(r"D:\Data\河北产品\微波辐射计\Z_UPAR_I_54510_20220508160000_P_YMWR_6000A_CP_M.txt")
#
# tem = ParseUtils.interpolate_tem(height, HEIGHT_83, tem_83)
# prs = ParseUtils.get_prs(height)
#
# print("高度:", height)
# print("温度：", tem)
# print("压强：", prs)
# print("风速：", w_speed)
# print("风向：", w_direct)
# pblh_result = pblh.get_pblh(height, tem, prs, w_speed, w_direct)
# VI_result = VI.get_VI(height, tem, prs, w_speed, w_direct)
# print("边界层高度：", pblh_result)
# print("边界层通风量：", VI_result)
def average(data):
    """"""
    array = np.array(data)
    summ = 0
    for i in array:
        summ += i
    return np.around(summ / len(array), 3)


def match_heights(wind_heights, lv2_heights, lv2_tempers):
    """
    将‘lv2高度层温度’插值为‘风廓线高度层温度’
    @param wind_heights: 风廓线数据高度层
    @param lv2_heights: lv2数据高度层（一般为83层）
    @param lv2_tempers: lv2高度层对应温度
    @return: 风廓线高度层对应温度
    """
    interped_tempers = []
    for wind_height in wind_heights:
        interped_temper = Lv2Utils.interp_tempers(wind_height, lv2_heights, lv2_tempers)
        interped_tempers.append(interped_temper)
    return interped_tempers

def average_datas(dir_path, interval=None, ):
    """
    根据时间间隔取向量均值
    @param interval: 时间间隔 单位：分钟
    @param dir_path: 风廓线数据目录
    """
    for root, _, files in os.walk(dir_path):
        # 记录起始时间
        # stime = WindUtils.minute_wind_time(files[0])
        # etime = stime + timedelta(minutes=interval)

        height = [120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 840, 960, 1080, 1200, 1320, 1440, 1560, 1680, 1800,
                  1920, 2040, 2160, 2280, 2400, 2520, 2640, 2760, 2880, 3000, 3120, 3240, 3360, 3480, 3600, 3720, 3840,
                  3960, 4080, 4320, 4560, 4800, 5040, 5280, 5520, 5760, 6000, 6240]
        directs, speeds = [], []
        for filename in files:
            if filename.endswith("ROBS.TXT"):
                filetime = WindUtils.minute_wind_time(filename)  # 提取文件名中的时间信息
                print(filetime)
                if interval:
                    # 记录起始时间
                    stime = WindUtils.minute_wind_time(files[0])
                    etime = stime + timedelta(minutes=interval)
                    if stime <= filetime <= etime:
                        df = ParseFiles.parse_minute_wind(os.path.join(root, filename))
                        ori_heights = df["height"].tolist()
                        ori_directs = df["hori_direct"].tolist()
                        ori_speeds = df["hori_speed"].tolist()

                        direct, speed = [], []
                        for h in height:
                            direct.append(WindUtils.interp_wdirect(h, ori_heights, ori_directs))
                            speed.append(WindUtils.interp_wspeed(h, ori_heights, ori_speeds))
                        directs.append(direct)
                        speeds.append(speed)

                    elif filetime > etime:
                        # 取平均
                        try:
                            aver_direct = average(directs)
                            aver_speed = average(speeds)

                            # 寻找对应时刻的lv2文件
                            lv2_dir = datetime.strftime(filetime, '%Y%m%d')
                            lv2_filename = f"Z_UPAR_I_54510_{datetime.strftime(filetime, '%Y%m%d%H%M%S')}_P_YMWR_6000A_CP_M.txt"
                            lv2_path = os.path.join(r"D:\PythonProject\hebei_product\Lv2数据", lv2_dir, lv2_filename)
                            # print(lv2_path)
                            # 提取lv2中的温度及高度
                            lv2_tempers, lv2_heights = Lv2Utils.get_tem_M(lv2_path)
                            # lv2温度 插值为 风廓线高度对应温度
                            wind_tempers = match_heights(height, lv2_heights, lv2_tempers)
                            # 压高公式转化
                            wind_pressures = MetCals.bat_height2prs(height)
                            pblh_rst = pblh.get_pblh(height, wind_tempers, wind_pressures, aver_speed, aver_direct)
                            vi_rst = VI.get_VI(height, wind_tempers, wind_pressures, aver_speed, aver_direct)
                            print(f"时间:{filetime}， 边界层高度：{pblh_rst}， 边界层通风量：{vi_rst}")
                        except ZeroDivisionError:
                            # print("取平均时除0")
                            pass
                        except FileNotFoundError:
                            # print(f"{filetime}时刻的lv2未找到")
                            pass
                        finally:
                            # 推进时间
                            stime = etime
                            etime = stime + timedelta(minutes=interval)
                            directs, speeds = [], []

                else:
                    # 风廓线数据
                    df = ParseFiles.parse_minute_wind(os.path.join(root, filename))
                    ori_heights = df["height"].tolist()
                    ori_directs = df["hori_direct"].tolist()
                    ori_speeds = df["hori_speed"].tolist()
                    print(f"风廓线有效数据维度：{len(ori_heights)}")
                    direct, speed = [], []
                    for h in height:
                        direct.append(WindUtils.interp_wdirect(h, ori_heights, ori_directs))
                        speed.append(WindUtils.interp_wspeed(h, ori_heights, ori_speeds))

                    # lv2数据
                    lv2_dir = datetime.strftime(filetime, '%Y%m%d')
                    lv2_filename = f"Z_UPAR_I_54510_{datetime.strftime(filetime, '%Y%m%d%H%M%S')}_P_YMWR_6000A_CP_M.txt"
                    lv2_path = os.path.join(r"D:\PythonProject\hebei_product\Lv2数据", lv2_dir, lv2_filename)
                    try:
                        lv2_tempers, lv2_heights = Lv2Utils.get_tem_M(lv2_path)
                    except FileNotFoundError:
                        print("文件不存在\n")
                        continue

                    # lv2温度 插值为 风廓线高度对应温度
                    tempers = match_heights(height, lv2_heights, lv2_tempers)
                    # 压高公式转化
                    pressures = MetCals.bat_height2prs(height)
                    Ris, plt_h = pblh.get_pblh(height, tempers, pressures, speed, direct)
                    # pblh_rst = pblh.get_pblh(height, tempers, pressures, speed, direct)
                    plt.plot(Ris, plt_h)
                    plt.xlabel("Ri/Rc")
                    plt.ylabel("h")
                    plt.savefig(rf"{filetime.strftime('%Y%m%d%H%M%S')}.jpg")
                    plt.close()
                    # print("边界层高度", pblh_rst, "\n")


if __name__ == '__main__':
    average_datas(r"D:\PythonProject\hebei_product\风廓线数据\风廓线绘图test", )
