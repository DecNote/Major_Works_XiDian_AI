import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import time
time_start = time.time()
global epsilon
global min_pit
#自定义参数：3个
epsilon = 0.5
min_pit = 10
file_name = 'b'  # 输入不同数据名以切换数据集
mat = scipy.io.loadmat(file_name+'.mat')
data_set = mat[file_name]
#参数定义
global number
number = data_set.shape[0]  # 样本个数
labels = data_set[:,2]  # 实际标签
global samples
samples = data_set[:,0:2]  # 样本集
global estimate_labels
estimate_labels = np.ones(labels.shape)*(-1)  # 估计标签
category = labels[-1] + 1
current_category = 0
def find_neighbors(f_sample):  # 寻找单个节点的邻居，返回邻居的列表
    neighbors = []
    i = 0
    for sample in samples:
        x = sample[0] - samples[f_sample,0]
        y = sample[1] - samples[f_sample,1]
        if ~(abs(x) > epsilon or abs(y) > epsilon):
            if np.linalg.norm(sample - samples[f_sample, :]) < epsilon:
                neighbors.append(i)
        i += 1
    return neighbors
def is_core(f_sample):
    neighbor = find_neighbors(f_sample)
    if len(neighbor) > min_pit:
        return 1
    else:
        return 0
def mark_neighbors(neighbours,category):   # 对核节点的邻居做标记
    for neighbour in neighbours:
        estimate_labels[neighbour] = category

def cluster(f_sample,category,i):
    sample_neighbor = find_neighbors(f_sample)
    if assist[f_sample,1] == 0:  # 判断是否是未被访问核节点
        assist[f_sample,1] = 1  # 标记该核节点已经被访问
        mark_neighbors(sample_neighbor,category)  # 标记邻居的类别
        sample_neighbor.remove(f_sample)
        for sample in sample_neighbor:
            cluster(sample,category,i+1)
global assist
assist = np.zeros([number,2])
for x in range(number):
    if len(find_neighbors(x)) > min_pit:
        assist[x,0] = 1
j = 1;
for x in range(number):
    if is_core(x) and assist[x,1] == 0:
        print(j);j=j+1
        cluster(x,current_category,1)
        current_category += 1
time_end = time.time()
print('Epsilon:',epsilon)
print('MinPit:',min_pit)
print('总样本数:',number)
print('核节点数:',sum(assist[:,0]))
print('划分类别数:',current_category)
print('孤立节点数：',sum(estimate_labels == -1),'(黑点表示)')
print('正确率:',np.sum(estimate_labels == labels) / number)
print('耗时:',time_end - time_start,'s')
color = ['blue','red','yellow','green','pink','white']
for x in range(current_category):
    plt.scatter(samples[estimate_labels == x, 0], samples[estimate_labels == x, 1], marker='.', color=color[x], s=6)
plt.scatter(samples[estimate_labels == -1, 0], samples[estimate_labels == -1, 1], marker='.', color='black', s=15)
plt.show()

