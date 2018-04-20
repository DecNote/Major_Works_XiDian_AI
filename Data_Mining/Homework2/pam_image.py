import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image
original_data = np.array(Image.open("pig2.jpg").convert('L'))
length=original_data.shape[1];width=original_data.shape[0]
global attributes
attributes=np.zeros(length*width)
for x in range(width):
    for y in range(length):
        attributes[x*length+y]=original_data[x,y]
classes=4
print(length,width)
estimate_class=np.zeros(length*width)
mid_sample=attributes[np.random.randint(length*width,size=classes)]
last_mid_sample=np.zeros(attributes.shape)

def caculate_cost( mid_sample,classes ):
    cost = 0
    counter=0
    for sample in attributes:
        if classes[counter]==0:
            cost=cost+abs(sample-mid_sample[0])
        elif classes[counter]==1:
            cost = cost + abs(sample - mid_sample[1])
        else:
            cost=cost+abs(sample-mid_sample[2])
        counter+=1
    return  cost

def cluster(mid_sample):
    counter = 0
    estimate_class=np.zeros(length*width)
    for attribute in attributes:
        distance = np.array([])
        for y in range(mid_sample.shape[0]):
            distance = np.hstack([distance, np.sum(abs(mid_sample[y] - attribute))])
        position = np.argwhere(distance == np.min(distance))
        estimate_class[counter] = position[0, 0]
        counter = counter + 1
    return estimate_class

estimate_class=cluster(mid_sample)
cost=caculate_cost(mid_sample,estimate_class)
last_cost=float("inf")
iteration=0
while cost<last_cost:
    last_cost=cost
    iteration+=1
    print('Iteration:',iteration)
    print('Cost:',cost)

    for x in range(classes):
        #建立临时变量
        temp_mid_sample = np.copy(mid_sample)
        #用原来的样本点逐个替换
        for sample in attributes:
            temp_mid_sample[x] = sample#替换中心点

            mark=(sample==mid_sample[classes-1]).all()
            for i in range(classes-1):
                mark=mark or (sample==mid_sample[i]).all()
            if ~mark:
                # 重新分类
                temp_estimate_class=cluster(temp_mid_sample)
                #重新计算损失
                temp_cost=caculate_cost(temp_mid_sample, temp_estimate_class)
                #print(temp_cost,cost)
                if temp_cost < cost:
                    estimate_class = np.copy(temp_estimate_class)
                    mid_sample = np.copy(temp_mid_sample)
                    cost=temp_cost
final_data=np.zeros(original_data.shape)
for x in range(width):
    for y in range(length):
        final_data[x,y]=estimate_class[x*length+y]*60
new_image=Image.fromarray(final_data)
new_image.show()
print('Iteration:',iteration)