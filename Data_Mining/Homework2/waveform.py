import numpy as np
with open("waveform.data") as file:
    lines=file.readlines()
data=[]
for line in lines:
    data.append([float(x) for x in line.split(',')])
array_data=np.array(data)
attributes=array_data[:,0:21]
classes=np.array([int(x) for x in array_data[:,-1]])
#pick 100 datapoints from each class
data_0=array_data[np.array([x==0 for x in classes])]
pick_data_0=array_data[np.random.randint(data_0.shape[0],size=100)]
data_1=array_data[np.array([x==1 for x in classes])]
pick_data_1=array_data[np.random.randint(data_1.shape[0],size=100)]
data_2=array_data[np.array([x==2 for x in classes])]
pick_data_2=array_data[np.random.randint(data_2.shape[0],size=100)]
#stack the pick datapoints in single array named pick_data
pick_data=np.vstack([pick_data_0,pick_data_1,pick_data_2])
pick_data_attributes=pick_data[:,0:-1]
estimate_class=np.zeros(300)
#genarate 3 middle samples from 300 samples picked
mid_sample=pick_data_attributes[np.random.randint(300,size=3)]
last_mid_sample=np.zeros([3,21])

iteration=0#record the times of iteration
while ~(last_mid_sample==mid_sample).all():
    last_mid_sample=np.copy(mid_sample)
    iteration+=1
    counter = 0
    for sample in pick_data_attributes:
        distance = np.array([])
        for x in range(0, 3):
            distance = np.hstack([distance, np.linalg.norm(mid_sample[x] - sample)])
        position = np.argwhere(distance == np.min(distance))
        estimate_class[counter] = position[0, 0]
        counter = counter + 1
    #update the new middle sample
    for x in range(0,3):
        mid_sample[x,:] = np.sum(pick_data_attributes[estimate_class == x], axis=0)/np.sum(estimate_class == x)
right_rate=np.sum(estimate_class==pick_data[:,-1])/300
print(right_rate)
print(iteration)
#print('RightRate:',right_rate)
#print('Iteration:',iteration)