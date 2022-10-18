from scipy.interpolate import interp1d


def A_index(data_press, data_temp, data_rhu):
    data_dewp = cal_dewp(data_temp, data_rhu)
    T500 = get_temp(500, data_press, data_temp)
    Td500 = get_dewp(500, data_press, data_dewp)
    T850 = get_temp(850, data_press, data_temp)
    Td850 = get_dewp(850, data_press, data_dewp)
    T700 = get_temp(700, data_press, data_temp)
    Td700 = get_dewp(700, data_press, data_dewp)
    A = (T850 - T500) - ((T850 - Td850) + (T700 - Td700) + (T500 - Td500))
    return round(A, 3)


def TT_Index(data_press, data_temp, data_rhu):
    """全总指数"""
    data_dewp = cal_dewp(data_temp, data_rhu)
    data = get_TT(data_press, data_temp, data_dewp)
    return data


def get_TT(data_press, data_temp, data_dewp):
    """
    计算全总指数(TT)
    :param data_press: 气压数据(列表)
    :param data_temp: 温度数据(列表)
    :param data_dewp: 露点数据(列表)
    """
    T500 = get_temp(500, data_press, data_temp)
    T850 = get_temp(850, data_press, data_temp)
    Td850 = get_dewp(850, data_press, data_dewp)
    TT = T850 + Td850 - 2 * T500
    return round(TT, 3)


def get_temp(press, data_press, data_temp):
    f = interp1d(data_press, data_temp, bounds_error=False, fill_value='extrapolate')
    temp = f(press)
    return temp


def get_dewp(press, data_press, data_dewp):
    f = interp1d(data_press, data_dewp, bounds_error=False, fill_value='extrapolate')
    dewp = f(press)
    return dewp


def cal_dewp(data_temp, data_rh):
    """
    给定温度和相对湿度，求出露点温度（列表或单个值）
    :param data_temp: 温度数据集
    :param data_rh: 相对湿度数据集
    :return: 露点温度
    """
    if isinstance(data_temp, list) and isinstance(data_rh, list):
        data_dewp = []
        list_zip = zip(data_temp, data_rh)
        for t, f in list_zip:
            x = 1 - 0.01 * f
            dpd = (14.55 + 0.114 * t) * x + ((2.5 + 0.007 * t) * x) ** 3 + (15.9 + 0.117 * t) * (x ** 14)
            Td = t - dpd
            data_dewp.append(round(Td, 3))
        return data_dewp
    else:
        x = 1 - 0.01 * data_rh
        dpd = (14.55 + 0.114 * data_temp) * x + ((2.5 + 0.007 * data_temp) * x) ** 3 + (15.9 + 0.117 * data_temp) * (
                x ** 14)
        Td = data_temp - dpd
        return round(Td, 3)
