import pblh
def get_VI(heights, temperatures, w_speeds):
    try:
        """计算边界层通风量, SFC为最底层高度"""
        VI = 0
        # sfc = heights[0]    # 最底层高度
        # pblh_value = pblh.get_pblh(heights, temperatures, pressures, w_speeds, w_directs)
        pblh_value = pblh.get_pblh2(heights, temperatures)

        for i in range(len(heights)):
            if i == 0:
                continue
            if heights[i] > pblh_value:
                break
            VI += w_speeds[i] * (heights[i] - heights[i-1])

        return round(VI, 3)
    except Exception as e:
        print(e)
