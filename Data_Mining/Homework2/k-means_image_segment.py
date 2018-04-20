import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image
original_data = np.array(Image.open("confidence1.jpg").convert('L'))
length=original_data.shape[1];width=original_data.shape[0]
data=np.zeros(length*width)
for x in range(width):
    for y in range(length):
        data[x*length+y]=original_data[x,y]
classes=4
mid_sample=data[np.random.randint(length*width,size=classes)]
last_mid_sample=np.zeros(mid_sample.shape)
estimate_class=np.zeros(length*width)
iteration=0
while ~(last_mid_sample==mid_sample).all():
    last_mid_sample=np.copy(mid_sample)
    iteration+=1
    print(iteration)
    counter = 0
    for sample in data:
        distance = np.array([])
        for x in range(0, classes):
            distance = np.hstack([distance, np.linalg.norm(mid_sample[x] - sample)])
        position = np.argwhere(distance == np.min(distance))
        estimate_class[counter] = position[0, 0]
        counter = counter + 1
    #update the new middle sample
    for x in range(0,classes):
        mid_sample[x] = np.sum(data[estimate_class == x])/np.sum(estimate_class == x)
final_data=np.zeros(original_data.shape)
for x in range(width):
    for y in range(length):
        final_data[x,y]=estimate_class[x*length+y]*60
new_image=Image.fromarray(final_data)
new_image.show()
print('Iteration:',iteration)