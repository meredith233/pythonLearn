

# ----------------------------------------------------------------------------------------------------------------------

# 数据集获取
# https://www.cs.utah.edu/~lifeifei/SpatialDataset.htm
# curl https://www.cs.utah.edu/\~lifeifei/research/tpq/NA.cnode > na_dataset.cnode
# 数据集坐标范围 [1, 10000]


# ----------------------------------------------------------------------------------------------------------------------
N = 100  # 数据集长


def init_dataset():
    InterestNodes = []  # 兴趣点集
    Nqi = []  # 各点Nqi
    Phi = []  # 各点Phi

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

    # 分配1000个兴趣点
    # Nqi中取前1000大坐标
    nqi_in_one = []
    for x in Nqi:
        for item in x:
            nqi_in_one.append(item)

    nqi_in_one = sorted(nqi_in_one, reverse=True)
    val = nqi_in_one[1000]

    for x1 in range(N):
        for y1 in range(N):
            if Nqi[x1][y1] > val and len(InterestNodes) < 1000:
                InterestNodes.append([x1, y1])
    print("数据集加载完成")
    return Phi, InterestNodes
