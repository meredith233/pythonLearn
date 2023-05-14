# ----------------------------------------------------------------------------------------------------------------------
import math
import random

# 数据集获取
# https://www.cs.utah.edu/~lifeifei/SpatialDataset.htm
# curl https://www.cs.utah.edu/\~lifeifei/research/tpq/NA.cnode > na_dataset.cnode
# 数据集坐标范围 [1, 10000]


# ----------------------------------------------------------------------------------------------------------------------

Kb = []
Ch = []


def by_phi(t):
    return t['phi']


def cal_kb(lu, phi):
    for x1 in range(lu[0] - 10, lu[0] + 10):
        for y1 in range(lu[1] - 10, lu[1] + 10):
            if x1 == lu[0] & y1 == lu[1]:
                continue
            if abs(phi[x1][y1] - phi[lu[0]][lu[1]]) < 0.0001:
                Kb.append([x1, y1])
            # else:
            #     if Phi[x1][y1] > Phi[Lu[0]][Lu[1]]:
            #         Sg.append([x1, y1])
            #     else:
            #         Sl.append([x1, y1])


def cal_ou(a, b):
    return math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2))


# x = int(input("用户位置x轴坐标:"))
# y = int(input("用户位置y轴坐标:"))
# Lu = [x, y]
def get_k(k, lu, phi):
    cal_kb(lu, phi)

    if len(Kb) >= k * 2:
        # 从G中随机选K个
        for i in range(k * 2 - 1):
            size = len(Kb)
            r = random.randint(0, size - 1)
            Ch.append(Kb[r])
            Kb.remove(Kb[r])
        Ch.append(lu)
    else:
        print('< K2')

    Clist = [lu]

    for i in range(k - 1):
        x = []
        maxNum = 0
        loc = []
        for h in Ch:
            val = 1
            for t in Clist:
                val = val * cal_ou(h, t)
            if val > maxNum:
                maxNum = val
                loc = h
        Clist.append(loc)
        Ch.remove(loc)
    return Clist
