import math

from alive_progress import alive_bar

# ----------------------------------------------------------------------------------------------------------------------

# 数据集获取
# https://www.cs.utah.edu/~lifeifei/SpatialDataset.htm
# curl https://www.cs.utah.edu/\~lifeifei/research/tpq/NA.cnode > na_dataset.cnode
# 数据集坐标范围 [1, 10000]

Nqi = []  # 各点Nqi /历史查询数
Phi = []  # 各点Phi /历史查询概率
W = 20
N = 100
K = 5
Rou = 0.01


# ----------------------------------------------------------------------------------------------------------------------


def init_dataset():
    nodes = []
    with open('na_dataset.cnode') as f:
        for line in f:
            temp = line.split(' ')
            x = float(temp[1])
            y = float(temp[2])
            nodes.append([x, y])
    # 初始化nqi
    # 数据集数据范围为 [0, 10000]
    # 均匀划分为 100 * 100 的坐标系内
    # 范围内点数作为nqi
    for x in range(100):
        for y in range(100):
            if y == 0:
                Nqi.append([])
            Nqi[x].append(1)

    for node in nodes:
        x = int(node[0] / 100) - 1
        y = int(node[1] / 100) - 1
        Nqi[x][y] += 1
    # 计算区域总查询数
    sum_nqi = 0
    for x1 in Nqi:
        for y1 in x1:
            sum_nqi += y1

    # 计算Phi
    for x1 in range(N):
        for y1 in range(N):
            if y1 == 0:
                Phi.append([])
            Phi[x1].append(Nqi[x1][y1] / sum_nqi)


# ----------------------------------------------------------------------------------------------------------------------


Lu = [0, 0]  # 用户所在位置
Zp = 0  # 用户所在位置查询概率
R = []  # 临时位置集, 将概率与Zp差值小于Rou的放入
Lc = []  # 匿名候选区


def cal_near_r():
    print("开始计算R")
    for x1 in range(N):
        for y1 in range(N):
            if Lu[0] == x1 & Lu[1] == y1:
                continue
            if math.fabs(Phi[x1][y1] - Zp) <= Rou:
                R.append([x1, y1])


def cal_ou(a, b):
    return math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2))


def by_dis(t):
    return t['dis']


def cal_near_loc():
    near = []
    print("开始计算Lc")
    for t in R:
        near.append({"loc": t, "dis": cal_ou(Lu, t)})
    near = sorted(near, key=by_dis)
    n = 1
    while n <= 2 * K - 2:
        n += 1
        Lc.append(near[n]['loc'])


# x = int(input("用户位置x轴坐标:"))
# y = int(input("用户位置y轴坐标:"))
# Lu = [x, y]
if __name__ == '__main__':
    init_dataset()  # 初始化数据集
    Zp = Phi[Lu[0]][Lu[1]]  # 用户所在位置查询概率
    cal_near_r()
    cal_near_loc()
    print(Lc)
