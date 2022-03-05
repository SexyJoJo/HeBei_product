import pandas as pd
import metpy.calc as mpcalc
from metpy.plots import SkewT
from metpy.units import units
import matplotlib.pyplot as plt
from dew_point import get_dewp


def plot_tlnp(tem, prs, rhu, wind_speed, wind_direct):
    """
    绘制t-lnp图
    :param tem:温度列表, 单位:摄氏度
    :param prs:压强列表, 单位:hPa
    :param rhu:相对湿度列表, 单位:%
    :param wind_speed:风速列表, 单位:海里
    :param wind_direct:风向列表, 单位:度

    """
    # 整理数据格式并分配单位
    T = pd.Series(tem).values * units.degC  # 温度
    p = pd.Series(prs).values * units.hPa   # 湿度
    Td = get_dewp(pd.Series(tem), pd.Series(rhu)).values * units.degC   # 露点温度
    # 得到风的分量
    wind_speed = pd.Series(wind_speed).values * units.knots
    wind_direct = pd.Series(wind_direct).values * units.degrees
    u, v = mpcalc.wind_components(wind_speed, wind_direct)

    # 设置绘图区
    fig = plt.figure(figsize=(9, 9))
    # 创建skew实例，这里的rotation=0参数十分重要，代表的意思是温度线与Y轴的夹角，0代表了国内的探空图，加上角度就变成了斜温图
    skew = SkewT(fig, rotation=30)
    # 设置横纵label
    skew.ax.set_ylabel('Height/hPa')
    skew.ax.set_xlabel('T/(℃)')
    # 画底图上的干绝热线、湿绝热线、饱和比湿线，可以注释掉，看看哪个是那个
    skew.plot_dry_adiabats()  # 干绝热线（红色虚线）
    skew.plot_moist_adiabats()  # 湿绝热线（蓝色虚线）
    skew.plot_mixing_lines()  # 饱和比湿线（绿色虚线）

    skew.plot(p, T, 'r')
    skew.plot(p, Td, 'g')
    skew.plot_barbs(p, u, v)

    # 计算抬升凝结的高度，返回位势高度，温度
    lcl_pressure, lcl_temperature = mpcalc.lcl(p[0], T[0], Td[0])
    # 根据温度和高度画个点，代表LCL
    skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')

    # 画状态曲线
    prof = mpcalc.parcel_profile(p, T[0], Td[0]).to('degC')
    skew.plot(p, prof, 'k', linewidth=2)

    # 画能量
    skew.shade_cin(p, T, prof)
    skew.shade_cape(p, T, prof)

    # # 画0度线
    # skew.ax.axvline(0, color='c', linestyle='--', linewidth=2)

    plt.show()


# 读取数据
df = pd.read_table(r'D:\PythonProject\EC_format_transform\Sounding\53996\2021\05\53996_20210501080000SURP.txt',
                   sep=' ', skiprows=1)
speeds = [10, 10, 10, 20, 20, 20, 12, 3, 3, 4, 4, 4, 2, 2, 40]
directions = [65, 65, 34, 67, 20, 13, 41, 12, 45, 6, 360, 270, 4, 45, 90]
plot_tlnp(df["TEM"], df["PRS_HWC"], df["RHU"], speeds, directions)
