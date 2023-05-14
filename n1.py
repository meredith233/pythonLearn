import math

from alive_progress import alive_bar

import utils

W = 20
N = 100
R = 0.5

# ----------------------------------------------------------------------------------------------------------------------

# 查询结果表
SearchRes = []
# 分区
Region = []
# 每个区域兴趣点
RegionInterests = []
# 每个区域点数量
RegionNode = []
# 区域间相似度
RegionR = []

Dire = [[0, 1], [0, -1], [1, 0], [-1, 0]]


def distance(x11, y11, x22, y22):
    return math.sqrt(math.pow(x11 - x22, 2) + math.pow(y11 - y22, 2))


def by_dis(t):
    return t['dis']


def set_nearest(xx, yy, source):
    source = sorted(source, key=by_dis)
    target = []
    for index in range(W):
        target.append(source[index]['index'])
    if yy == 0:
        SearchRes.append([])
    SearchRes[xx].append(target)


# 相同点个数
def common(list1, list2):
    list1 = sorted(list1)
    list2 = sorted(list2)
    ii = 0
    j = 0
    count = 0
    while ii < W and j < W:
        if list1[ii] == list2[j]:
            count += 1
            ii += 1
            j += 1
        elif list1[ii] > list2[j]:
            j += 1
        elif list1[ii] < list2[j]:
            ii += 1
    return count


def check_limit(xx, yy):
    if xx < 0:
        return False
    if yy < 0:
        return False
    if xx >= N:
        return False
    if yy >= N:
        return False
    return True


def dfs(xx, yy, index):
    for move in Dire:
        xm = xx + move[0]
        ym = yy + move[1]
        flag = check_limit(xm, ym)
        if not flag:
            # 超出边界，跳过
            continue
        if Region[xm][ym] != -1:
            # 已有分区，跳过
            continue
        cc = common(SearchRes[xx][yy], SearchRes[xm][ym])
        if cc == W:
            # 相似度为1
            Region[xm][ym] = index
            RegionNode[index] += 1
            dfs(xm, ym, index)


# 结算每个点查询结果
def cal_search_res(interest_nodes):
    print("开始计算各点查询结果")
    with alive_bar((N * N * len(interest_nodes)), force_tty=True, length=20) as bar:
        for x in range(N):
            for y in range(N):
                near = []
                for i in range(len(interest_nodes)):
                    interest = interest_nodes[i]
                    near.append({"index": i, "dis": distance(x, y, interest[0], interest[1])})
                    bar()
                set_nearest(x, y, near)
    del near, x, y, i, interest
    print("\n")


def distribute_region():
    # 初始化region组全为-1
    for x1 in range(N):
        for y1 in range(N):
            if y1 == 0:
                Region.append([])
            Region[x1].append(-1)

    region_count = 0
    # 运用dfs来进行分区
    for x1 in range(N):
        for y1 in range(N):
            if Region[x1][y1] != -1:
                continue
            Region[x1][y1] = region_count
            RegionNode.append(1)
            RegionInterests.append(SearchRes[x1][y1])
            dfs(x1, y1, region_count)
            region_count += 1
    del x1, y1
    print("分区数 ", region_count)
    return region_count


def cal_region_relate(region_count):
    # 计算分区相似度表T -> regionR
    print('开始计算分区相似度')
    with alive_bar(region_count * region_count, force_tty=True, length=20) as bar:
        for x1 in range(region_count):
            for x2 in range(region_count):
                if x2 == 0:
                    RegionR.append([])
                c = common(RegionInterests[x1], RegionInterests[x2])
                RegionR[x1].append(round(c / W, 2))
                bar()
    print("\n")


# 前期准备完成------------------------------------------------------------------------------------------------------------


# 选择匿名候选分区
def cal_acr(user_loc, region_total, k):
    # 用户所在分区
    zu = Region[user_loc[0]][user_loc[1]]

    # 将Zu与其他分区服务相似度降序排列
    def by_r(tt):
        return tt['r']

    temp = []
    for index in range(region_total):
        if index == zu:
            continue
        temp.append({"index": index, "r": RegionR[zu][index]})
    zi_list = sorted(temp, key=by_r, reverse=True)
    acr_temp = [zu]

    index = 0
    loc_num = RegionNode[zu]
    # 如果分区中的位置数量小于2k+1，考虑更换分区
    while loc_num < 2 * k + 1:

        zi_item = zi_list[index]
        index += 1
        if zi_item['r'] >= R:
            zone = zi_item['index']
            loc_num += RegionNode[zone]
            acr_temp.append(zone)  # 没有选不出来的解决方案
    # 输出结果
    # print("Acr计算完成 " + str(acr_temp))
    return acr_temp


def get_region_list(zone):
    temp_list = []
    for xx in range(N):
        for yy in range(N):
            for z in zone:
                if Region[xx][yy] == z:
                    temp_list.append([xx, yy])
                    break
    return temp_list


# 扰动位置生成
# acr 分区
# user_loc 用户位置
def cal_fake_loc(acr_list, user_loc, k, phi):
    a_s = [user_loc]
    acr_list = get_region_list(acr_list)  # acr所在分区所有点坐标集合
    acr_list.remove(user_loc)
    for it in range(k - 1):  # 选择k-1次
        v = []  # 坐标值
        e_max = 0  # 最大熵
        for j in acr_list:
            a_s.append(j)
            e_as = utils.cal_e(a_s, phi)

            if e_as > e_max:
                e_max = e_as
                v = j
            a_s.remove(j)

        # print('第', it, '次选择')
        # print('选择点: ', v)
        # print('最大熵: ', e_max)
        if v:
            a_s.append(v)
            acr_list.remove(v)

    return a_s


def init(interest_nodes):
    cal_search_res(interest_nodes)  # 计算各点查询结果  从此开始受W影响
    region_num = distribute_region()  # 将查询结果相同点点放到同一分区
    cal_region_relate(region_num)  # 计算分区相似度
    return region_num


def get_k(lu, k, region_num, phi):
    acr = cal_acr(lu, region_num, k)  # 计算匿名候选区 从此开始受K/R影响
    return cal_fake_loc(acr, lu, k, phi)  # 计算匿名位置集
