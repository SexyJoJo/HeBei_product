import pblh
def get_VI(heights, temperatures, pressures, w_speeds, w_directs):
    try:
        """计算边界层通风量, SFC为最底层高度"""
        VI = 0
        # sfc = heights[0]    # 最底层高度
        pblh_value = pblh.get_pblh(heights, temperatures, pressures, w_speeds, w_directs)

        for i in range(len(heights)):
            if i == 0:
                continue
            if heights[i] > pblh_value:     # TODO 可能需要插值pblh高度对应的风速
                break
            VI += w_speeds[i] * (heights[i] - heights[i-1])

        return round(VI, 3)
    except Exception as e:
        print(e)
