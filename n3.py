import math
import random


N = 100

# ----------------------------------------------------------------------------------------------------------------------


def by_phi(t):
    return t['phi']


def cal_h(lu, phi, k):
    G = []
    Gsub = []
    h = []
    for x1 in range(N):
        for y1 in range(N):
            if x1 == lu[0] & y1 == lu[1]:
                continue
            if phi[x1][y1] == phi[lu[0]][lu[1]]:
                G.append([x1, y1])
            else:
                Gsub.append({"phi": phi[x1][y1], "loc": [x1, y1]})
    Gsub = sorted(Gsub, key=by_phi, reverse=True)

    # 从G中随机选K个
    for i in range(k):
        size = len(G)
        r = random.randint(0, size - 1)
        h.append(G[r])
        G.remove(G[r])
    # 从sub中选前K个
    for i in range(k):
        h.append(Gsub[i]['loc'])
    return h


def cal_ou(a, b):
    return math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2))


def cal_c1(lu, h):
    far = 0
    c = []
    for x in h:
        ou = cal_ou(lu, x)
        if ou > far:
            far = ou
            c = x
    return c


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


# 在H剩下的点中选择 k - 2 个点
def cal_ans(k, h, ans):
    for i in range(k - 2):
        area = 0
        loc = []
        for x in h:
            points = []
            for temp in ans:
                points.append(temp)
            points.append(x)
            t = get_area(points)
            if t > area:
                area = t
                loc = x
        ans.append(loc)
        h.remove(loc)


# x = int(input("用户位置x轴坐标:"))
# y = int(input("用户位置y轴坐标:"))
# Lu = [x, y]

def get_k(lu, phi, k):
    ans = []
    h = cal_h(lu, phi, k)
    c1 = cal_c1(lu, h)
    h.remove(c1)
    ans.append(lu)
    ans.append(c1)

    cal_ans(k, h, ans)
    return ans
