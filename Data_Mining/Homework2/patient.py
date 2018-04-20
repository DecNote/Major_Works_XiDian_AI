import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
blood=np.array([830,1900,200])
plt.pie(blood,labels=["去白细胞悬浮红细胞","冷沉淀凝血因子","白细胞单采小板"],autopct='%.0f%%', shadow=True)
plt.show()
