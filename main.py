import dataset
import n1
import n2
import n3
import matplotlib

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

Phi, InterestNodes = dataset.init_dataset()
RegionNum = n1.init(InterestNodes)

print('初始化数据完成')

Lu = [25, 25]
n = 4
x = []
y1 = []
y2 = []
y3 = []
yy1 = []
yy2 = []
yy3 = []
while n <= 30:
    n += 1
    K = n
    x.append(K)
    L1 = n1.get_k(Lu, K, RegionNum, Phi)
    L2 = n2.get_k(K, Lu, Phi)
    L3 = n3.get_k(Lu, Phi, K)
    y1.append(n3.get_area(L1))
    y2.append(n3.get_area(L2))
    y3.append(n3.get_area(L3))
    yy1.append(n1.cal_e(L1, Phi))
    yy2.append(n1.cal_e(L2, Phi))
    yy3.append(n1.cal_e(L3, Phi))

# encoding=utf-8

# mpl.rcParams['font.sans-serif'] = ['SimHei']
print(y1)
print(y2)
print(y3)
names = ['5', '10', '15', '20', '25']
plt.subplot(2, 1, 1)
plt.plot(x, y1, marker='x', mec='r', mfc='w', label=u'1')
plt.plot(x, y2, marker='o', mec='r', mfc='w', label=u'2')
plt.plot(x, y3, marker='*', ms=10, label=u'3')
plt.legend()  # 让图例生效
# plt.xticks(x, names, rotation=45)
# plt.margins(0)
# plt.subplots_adjust(bottom=0.15)
plt.xlabel("k")  # X轴标签
plt.ylabel("area")  # Y轴标签
# plt.title("area")  # 标题


print(yy1)
print(yy2)
print(yy3)
plt.subplot(2, 1, 2)
plt.plot(x, yy1, marker='x', mec='r', mfc='w', label=u'1')
plt.plot(x, yy2, marker='o', mec='r', mfc='w', label=u'2')
plt.plot(x, yy3, marker='*', ms=10, label=u'3')
plt.legend()  # 让图例生效
plt.xlabel("k")  # X轴标签
plt.ylabel("e")  # Y轴标签

plt.show()
