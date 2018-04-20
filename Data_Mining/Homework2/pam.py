import numpy as np
with open('waveform-+noise.data')as file:
    lines = file.readlines()
data=[]
for line in lines:
    data.append([float(x) for x in line.split(',')])

array_data=np.array(data)
array_data=np.copy(array_data[0:500,:])

global attributes
attributes=array_data[:,0:40]
classes=np.array([int(x) for x in array_data[:,-1]])
estimate_class=np.zeros(array_data.shape[0])
mid_sample=attributes[np.random.randint(array_data.shape[0],size=3)]
last_mid_sample=np.zeros(attributes.shape)

def caculate_cost( mid_sample,classes ):
    cost = 0
    counter=0
    for sample in attributes:
        if classes[counter]==0:
            cost=cost+sum(abs(sample-mid_sample[0,:]))
        elif classes[counter]==1:
            cost = cost + sum(abs(sample - mid_sample[1,:]))
        else:
            cost=cost+sum(abs(sample-mid_sample[2,:]))
        counter+=1
    return  cost

def cluster(mid_sample):
    counter = 0
    estimate_class=np.zeros(attributes.shape[0])
    for attribute in attributes:
        distance = np.array([])
        for y in range(3):
            distance = np.hstack([distance, np.sum(abs(mid_sample[y, :] - attribute))])
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
    print('RightRate:',sum(estimate_class==classes)/500)

    for x in range(3):
        #建立临时变量
        temp_mid_sample = np.copy(mid_sample)
        #用原来的样本点逐个替换
        for sample in attributes:
            temp_mid_sample[x,:] = sample#替换中心点
            mark=(sample==mid_sample[1,:]).all() or (sample==mid_sample[2,:]).all() or (sample==mid_sample[0,:]).all()
            if ~mark:
                # 重新分类
                temp_estimate_class=cluster(temp_mid_sample)
                #重新计算损失
                temp_cost=caculate_cost(temp_mid_sample, temp_estimate_class)
                if temp_cost < cost:
                    estimate_class = np.copy(temp_estimate_class)
                    mid_sample = np.copy(temp_mid_sample)
                    cost=temp_cost
print('\nFinal RightRate:', sum(estimate_class == classes) / 500)
