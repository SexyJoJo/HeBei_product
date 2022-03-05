def get_dewp(data_temp, data_rh):
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