def get_IOI(heights, temperatures):
    """
    计算逆温强度
    :param temperatures: 索引为高度（km）， 值为温度（℃） 的Series
    :return: [[底高1，顶高1，逆温厚度1, 逆温差1, 逆温强度1], [底高2, 顶高2, 逆温厚度2, 逆温差2, 逆温强度2], ... ](可能出现多个逆温层)
    """
    # heights = list(map(lambda x: float(x) / 1000, heights))
    # temperatures = pd.Series(temperatures, heights)
    results = []    # 存放各逆温层的逆温强度
    i = 0
    while i < len(temperatures) - 1:
        # 气温随高度增加而下降，未发生逆温
        if temperatures[i] >= temperatures[i + 1]:
            i += 1
            continue
        # 气温随高度增加而增加，出现逆温
        else:
            # 逆温层底高H1:逆温层起始点高度
            H1 = float(heights[i]) * 10  # 单位：米
            T1 = float(temperatures[i])
            # 寻找顶高H2：逆温层中止点高度
            while temperatures[i] < temperatures[i + 1]:
                if i == len(temperatures) - 2:
                    i += 1
                    break
                i += 1
            H2 = float(heights[i])  # 单位：米
            T2 = float(temperatures[i])
            delta_H = H2 - H1
            delta_T = T2 - T1

            # 温差大于1视为存在逆温层
            if delta_T > 1:
                result = [H1, H2, delta_H, delta_T, round(delta_T / delta_H, 3)]
                results.append(result)
    return results
