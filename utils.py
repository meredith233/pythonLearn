import math


def cal_e(a_s, phi):
    sum_phi = 0
    for loc in a_s:
        sum_phi += phi[loc[0]][loc[1]]

    e = 0
    for loc in a_s:
        phi_val = phi[loc[0]][loc[1]]
        if phi_val == 0:
            continue
        pj = phi_val / sum_phi
        e -= pj * math.log(pj, 2)
    return e

def get_area(points):
    # 基于向量叉乘计算多边形面积
    area = 0
    for i in range(0, len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]

        triArea = (p1[0] * p2[1] - p2[0] * p1[1]) / 2
        # print(triArea)
        area += triArea

    fn = (points[-1][0] * points[0][1] - points[0][0] * points[-1][1]) / 2
    # print(fn)
    return abs(area + fn)