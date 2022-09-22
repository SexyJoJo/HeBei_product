import math

def get_u(speed, direct):
    return speed * math.sin(direct)

def get_v(speed, direct):
    return speed * math.cos(direct)

def cal_ang(point_1, point_2, point_3):
    """
    根据三点坐标计算夹角
    :param point_1: 点1坐标
    :param point_2: 点2坐标
    :param point_3: 点3坐标
    :return: 返回最大夹角
    """
    a = math.sqrt(
        (point_2[0] - point_3[0]) * (point_2[0] - point_3[0]) + (point_2[1] - point_3[1]) * (point_2[1] - point_3[1]))
    b = math.sqrt(
        (point_1[0] - point_3[0]) * (point_1[0] - point_3[0]) + (point_1[1] - point_3[1]) * (point_1[1] - point_3[1]))
    c = math.sqrt(
        (point_1[0] - point_2[0]) * (point_1[0] - point_2[0]) + (point_1[1] - point_2[1]) * (point_1[1] - point_2[1]))
    A = math.degrees(math.acos((a * a - b * b - c * c) / (-2 * b * c)))
    B = math.degrees(math.acos((b * b - a * a - c * c) / (-2 * a * c)))
    C = math.degrees(math.acos((c * c - a * a - b * b) / (-2 * a * b)))
    return round(max([A, B, C]), 2)


def get_divergence(site1, site2, site3):
    """计算散度
    site = (x, y, 风速, 风向)"""
    if len(site1) != 4 or len(site2) != 4 or len(site3) != 4:
        raise Exception("元组缺少要素, 分别需要（经度坐标，纬度坐标，风速，风向）组成一个元组")

    # site转为[x, y, u, v]
    site1 = list(site1)
    site2 = list(site2)
    site3 = list(site3)

    speed1, direct1 = site1[2], site1[3]
    speed2, direct2 = site2[2], site2[3]
    speed3, direct3 = site3[2], site3[3]
    site1[2], site1[3] = get_u(speed1, direct1), get_v(speed1, direct1)
    site2[2], site2[3] = get_u(speed2, direct2), get_v(speed2, direct2)
    site3[2], site3[3] = get_u(speed3, direct3), get_v(speed3, direct3)

    max_angle = cal_ang((site1[0], site1[1]), (site2[0], site2[1]), (site3[0], site3[1]))
    divergence = ((site2[2] - site1[2]) * (site3[1] - site1[1]) - (site3[2] - site1[2]) * (site2[1] - site1[1]) +
                  (site2[0] - site1[0]) * (site3[3] - site1[3]) - (site3[0] - site1[0]) * (site2[3] - site1[3])) / \
                 ((site2[0] - site1[0]) * (site3[1] - site1[1]) - (site3[0] - site1[0]) * (site2[1] - site1[1]))
    return round(divergence, 3), max_angle


def get_vorticity(site1, site2, site3):
    if len(site1) != 4 or len(site2) != 4 or len(site3) != 4:
        raise Exception("元组缺少要素, 分别需要（经度坐标，纬度坐标，风速， 风向）组成一个元组")

    # site转为[x, y, u, v]
    site1 = list(site1)
    site2 = list(site2)
    site3 = list(site3)

    speed1, direct1 = site1[2], site1[3]
    speed2, direct2 = site2[2], site2[3]
    speed3, direct3 = site3[2], site3[3]
    site1[2], site1[3] = get_u(speed1, direct1), get_v(speed1, direct1)
    site2[2], site2[3] = get_u(speed2, direct2), get_v(speed2, direct2)
    site3[2], site3[3] = get_u(speed3, direct3), get_v(speed3, direct3)

    max_angle = cal_ang((site1[0], site1[1]), (site2[0], site2[1]), (site3[0], site3[1]))
    vorticity = ((site2[3] - site1[3]) * (site3[1] - site1[1]) - (site3[3] - site1[3]) * (site2[1] - site1[1]) +
                 (site2[0] - site1[0]) * (site3[2] - site1[2]) - (site3[0] - site1[0]) * (site2[2] - site1[2])) / \
                ((site2[0] - site1[0]) * (site3[1] - site1[1]) - (site3[0] - site1[0]) * (site2[1] - site1[1]))
    return round(vorticity, 3), max_angle
