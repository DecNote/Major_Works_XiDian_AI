import numpy as np
import scipy.io
import matplotlib.pyplot as plt
#文件名
file_name = 'square1'
mat = scipy.io.loadmat(file_name+'.mat')
data_set = mat[file_name]
labels = data_set[:, 2]  # 实际标签
samples = data_set[:, 0:2]  # 样本集
category_number = labels[-1]
color = ['blue', 'red', 'yellow', 'green', 'pink', 'white']
for x in range(int(category_number + 1)):
    plt.scatter(samples[labels == x,0], samples[labels == x,1], marker='.', color=color[x], s = 6)
plt.show()