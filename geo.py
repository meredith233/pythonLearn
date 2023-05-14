import math
import random

import utils

N = 1000

# ----------------------------------------------------------------------------------------------------------------------


def by_phi(t):
    return t['phi']


def cal_h(lu, phi, k):
    G = []
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
    # 在 Ｇ 中，从用户左侧 随 机 选 取 Ｋ 个 位 置 单 元，并 从 用 户 右 侧
    # 顺序选取 Ｋ 个位置单元，将这２Ｋ 个位置单元放入队列 Ｈ 中。
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


# 从队列 Ｈ 中选择一个距用户最远的位置单元作为第 １个 假
# 位置 Ｃ１。
def cal_c1(lu, h):
    far = 0
    c = []
    for x in h:
        ou = cal_ou(lu, x)
        if ou > far:
            far = ou
            c = x
    return c


# 在H剩下的点中选择 k - 2 个点
def cal_ans(k, h, ans):
    # 每次取能围成最大面积的一个点
    for i in range(k - 2):
        area = 0
        loc = []
        for x in h:
            points = []
            for temp in ans:
                points.append(temp)
            points.append(x)
            t = utils.get_area(points)
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
