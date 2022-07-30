import os.path

import numpy as np
import pandas as pd
from datetime import datetime
from scipy.interpolate import interp1d


# class ParseUtils:
#     """解析工具类"""
#     @staticmethod
#     def get_height_speed_direct(path):
#         wind_df = pd.read_table(path, sep=' ')
#         heights = wind_df["Heigh_Alti"].tolist()
#         w_speeds = wind_df["WIN_S"].tolist()
#         w_directs = wind_df["WIN_D"].tolist()
#
#         drop = []
#         for i in range(len(heights)):
#             if w_speeds[i] > 9999 or w_directs[i] > 9999:
#                 drop.append(i)
#
#         for i in drop[::-1]:
#             del heights[i]
#             del w_speeds[i]
#             del w_directs[i]
#         return heights, w_speeds, w_directs
#
# @staticmethod
# def get_tem_M(path):
#     df = pd.read_csv(path, skiprows=2, encoding='gbk')
#     line = df[df['10'] == 11].iloc[0].tolist()[11: -1]
#     line = [round(x, 3) for x in line]
#
#     heights = df.columns[11:-1]
#     heights = [int(float(x[:-4]) * 1000) for x in heights]
#     return line, heights
#
#     @staticmethod
#     def get_prs(heights):
#         def height2prs(height):
#             return round(pow(1 - height / 44331, 1.0 / 0.1903) * 1013.25, 3)
#
#         rst = []
#         for h in heights:
#             rst.append(height2prs(h))
#         return rst
#
#     @staticmethod
#     def interpolate_speed(heights, w_speeds):
#         rst = []
#         for h in HEIGHT_83:
#             sp = pblh.interp_wspeed(h, heights, w_speeds)
#             rst.append(round(float(sp), 3))
#         return rst
#
#     @staticmethod
#     def interpolate_tem(heights, Height_83, temperature_83):
#         rst = []
#         for h in heights:
#             sp = pblh.get_temp(h, Height_83, temperature_83)
#             rst.append(round(float(sp), 3))
#         return rst
#
#     @staticmethod
#     def interpolate_direct(heights, w_directs):
#         rst = []
#         for h in HEIGHT_83:
#             dr = pblh.interp_wdirect(h, heights, w_directs)
#             rst.append(round(float(dr), 3))
#         return rst
class MetCals:
    """气象计算工具"""
    @staticmethod
    def prs2height(prs):
        return round(44331 * (1 - (prs / 1013.25) ** 0.1903), 3)

    @staticmethod
    def height2prs(height):
        return round(pow(1 - height / 44331, 1.0 / 0.1903) * 1013.25, 3)

    @staticmethod
    def bat_prs2height(pressures):
        """
        气压列表批量转化为高度列表
        @param pressures: 气压列表 单位：hPa
        @return: 高度列表 单位：m
        """
        heights = []
        for prs in pressures:
            heights.append(MetCals.prs2height(prs))
        return heights

    @staticmethod
    def bat_height2prs(heights):
        """
        高度列表批量转化为气压列表
        @param heights: 高度列表 单位：m
        @return: 气压列表 单位：hPa
        """
        pressures = []
        for height in heights:
            pressures.append(MetCals.height2prs(height))
        return pressures

    @ staticmethod
    def get_potem(t, p):
        """
        获得未饱和湿位温(Potential temperature)(°C)  位温定义为空气沿干绝热线过程变化到气压p=1000hPa时的温度（天气分析 P16）
        :param t: 气温(°C)
        :param p: 气压(mb)
        """
        theta = (t + 273.15) * ((1000 / p) ** 0.286) - 273.15  # (°C) C#的公式减273.15
        return theta


class Lv2Utils:
    """微波辐射计Lv2解析工具类"""
    @staticmethod
    def get_time(filename, kind="datetime"):
        """
        从LV2文件名中提取时间信息
        @param filename: 文件名
        @param kind: 时间的类型（字符串 or datetime对象）
        @return: datetime对象
        """
        string = filename.split("_")[4]
        time = datetime.strptime(string, "%Y%m%d%H%M%S")
        if kind == "datetime":
            return time

        time_str = datetime.strftime(time, "%Y-%m-%d %H:%M:%S")
        return time_str

    @staticmethod
    def get_tem_M(path):
        """
        从分钟级Lv2数据中提取温度列表和对应高度列表
        @param path: lv2分钟级文件路径
        @return: 温度列表、 高度列表
        """
        if not (path.endswith("CP_M.txt") or path.endswith("CP_M.TXT")):
            raise Exception("未输入CP_M文件")

        df = pd.read_csv(path, skiprows=2, encoding='gbk')
        tempers = df[df['10'] == 11].iloc[0].tolist()[11: -1]
        tempers = [round(x, 3) for x in tempers]

        heights = df.columns[11:-1]
        heights = [int(float(x[:-4]) * 1000) for x in heights]
        return tempers, heights

    @staticmethod
    def get_tem_D(path):
        """
        从日级LV2数据中提取温度dataframe和高度列表
        @param path: lv2日级文件路径
        @return: 温度dataframe、高度列表
        """
        if path.endswith("QC.csv"):
            df = pd.read_csv(path, encoding='gbk')
            tempers = df[df['10'] == 11]
            heights = df.columns[11:-1]
            heights = [int(float(x[:-3]) * 1000) for x in heights]
        else:
            df = pd.read_csv(path, skiprows=2, encoding='gbk')
            tempers = df[df['10'] == 11]
            heights = df.columns[11:-1]
            heights = [int(float(x[:-4]) * 1000) for x in heights]
        return tempers, heights

    @staticmethod
    def interp_tempers(height, data_height, data_tempers):
        """
        根据高度列表插值温度
        @param height: 待插值的高度
        @param data_height: 高度列表
        @param data_tempers: 温度列表
        @return: height对应的温度
        """
        f = interp1d(data_height, data_tempers, bounds_error=False, fill_value='extrapolate')
        return float(f(height))


class WindUtils:
    """风廓线数据解析工具类"""
    @staticmethod
    def minute_wind_time(filename):
        """
        根据文件名提取观测时间
        @param filename: 文件名
        @return: datetime时间对象
        """
        info = filename.split("_")
        time = datetime.strptime(info[4], "%Y%m%d%H%M%S")
        return time

    @staticmethod
    def interp_wspeed(height, data_height, data_wspeeds):
        """
        根据高度列表插值风速
        @param height: 待插值的高度
        @param data_height: 高度列表
        @param data_wspeeds: 风速列表
        @return: height对应的风速
        """
        f = interp1d(data_height, data_wspeeds, bounds_error=False, fill_value='extrapolate')
        if f(height) <= 0:
            return 0.1
        return float(f(height))

    @staticmethod
    def interp_wdirect(height, data_height, data_wdirect):
        """
        根据高度列表插值风向
        @param height: 待插值的高度
        @param data_height: 高度列表
        @param data_wdirect: 风向列表
        @return: height对应的风向
        """
        try:
            for i in range(len(data_wdirect) - 1):
                if data_wdirect[i] > 270 and data_wdirect[i + 1] < 90:
                    i = i + 1
                    while data_wdirect[i] < 90:
                        data_wdirect[i] += 360
                        i += 1
                elif data_wdirect[i] < 90 and data_wdirect[i + 1] > 270:
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
        return float(w_dircect)


class SoundingUtils:
    """探空文件数据处理工具类"""
    @staticmethod
    def interp_tempers(height, data_height, data_tempers):
        """
        根据高度列表插值温度
        @param height: 待插值的高度
        @param data_height: 高度列表
        @param data_tempers: 温度列表
        @return: height 对应的温度
        """
        f = interp1d(data_height, data_tempers, bounds_error=False, fill_value='extrapolate')
        return float(f(height))

    @ staticmethod
    def cap_by_height(df, end_h, start_h=0):
        """
        根据起始与结束高度截取探空dataframe
        @param df: 待截取的探空dataframe
        @param start_h: 起始高度，默认为0 单位：m
        @param end_h: 结束高度 单位：m
        @return: 截取后的dataframe
        """
        if start_h == 0:
            df = df[df["GPH"] >= start_h]
        return df[df["GPH"] <= end_h]


class ParseFiles:
    """解析文件类"""
    @staticmethod
    def cap_week_wind(file_path, station, time_str):
        """
        根据时间和站号，从风廓线周数据中提取对应数据片段并保存于Data目录下
        @param file_path: 待截取的风廓线周数据文件路径
        @param station: 截取文件的站号
        @param time_str: 截取的时间字符串
        """
        full_df = pd.read_json(file_path)
        df = pd.DataFrame()
        for i in full_df['DS']:
            if i["Station_Id_C"] == str(station) and i["Datetime"] == time_str:
                temp_df = pd.DataFrame(i, index=[0])
                temp_df['Heigh_Alti'] = temp_df['Heigh_Alti'].astype(int)
                df = pd.concat([df, temp_df], axis=0)
        df = df.sort_values(by='Heigh_Alti')
        if not os.path.exists(r"Data"):
            os.mkdir(r"Data")
        df.to_csv(rf"./Data/wind_{station}_{time_str[:10] + time_str[11:13]}.txt", sep=" ", index=False)
        print(df)

    @staticmethod
    def parse_minute_wind(file_path):
        """
        解析分钟级风廓线雷达数据
        @param file_path: 风廓线雷达文件名
        @return: datafarme
        """
        df = pd.read_csv(
            file_path, skiprows=3, sep=r'\s+',
            names=["height", "hori_direct", "hori_speed", "verti_speed", "hori_credi", "verti_credi", "Cn2"]
        )
        df = df.replace("/////", np.nan)
        df = df.replace("////////", np.nan)
        df.dropna(axis=0, how="any", inplace=True)
        df = df.astype({"height": int, "hori_direct": float, "hori_speed": float, "verti_speed": float,
                        "hori_credi": int, "verti_credi": int, "Cn2": float})
        return df

    @staticmethod
    def parse_sounding(file_path):
        """
        解析探空数据
        @param file_path:
        @return:dataframe
        """
        df = pd.read_csv(file_path, skiprows=1, sep=r'\s+')
        return df
