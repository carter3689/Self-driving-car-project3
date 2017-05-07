import csv
import cv2
import numpy as np
from keras.preprocessing.image import img_to_array, load_img
lines = []
with open('./data/driving_log_1.csv')as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        lines.append(line)

images = []
measurements = []
for line in lines:
    for i in range(3):
        source_path = line[i]
        file_name = source_path.split('/')[-1]
        current_path = 'data/IMG/' + file_name 
        image = cv2.imread(current_path)
        #image = cv2.cvtColor(image, 1)
    if image == None:
        continue
    images.append(image)
    measurement = float(line[3])
    measurements.append(measurement)
print(len(images))


##### Testing images array ######
X_train = np.array(images)
print(X_train.shape)
y_train = np.array(measurements)


from keras.models import Sequential
from keras.layers import Flatten,Dense


###### flipping images #####
augmented_images, augmented_measurements = [],[]
for image, measurement in zip(images, measurements):
    augmented_images.append(image)
    augmented_measurements.append(measurement)
    augmented_images.append(cv2.flip(image,1))
    augmented_measurements.append(measurement*-1.0)

X_train = np.array(augmented_images)
print(X_train.shape)

y_train = np.array(augmented_measurements)


print(len(X_train))
print(X_train.shape)

from keras.models import Sequential
from keras.layers import Flatten,Dense, Lambda,Cropping2D
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D
from keras.layers.normalization import BatchNormalization

model = Sequential()
model.add(Lambda(lambda x: x / 255.0 - 0.5, input_shape=(160,320,3)))
model.add(Cropping2D(cropping=((70,25),(0,0))))
model.add(Convolution2D(24,5,5,subsample=(2,2),activation="elu"))
model.add(Convolution2D(36,5,5,subsample=(2,2),activation="elu"))
model.add(Convolution2D(48,5,5,subsample=(2,2),activation="elu"))
model.add(Flatten())
model.add((Dense(100)))
model.add(BatchNormalization())
model.add((Dense(50)))
model.add((Dense(10)))
model.add((Dense(1)))


model.compile(loss='mse', optimizer = 'adam')
model.fit(X_train,y_train,validation_split=0.2, shuffle=True,nb_epoch=5)

#keras.callbacks.ModelCheckpoint('/home/ubuntu/model.h5', monitor='val_loss', verbose=0, save_best_only=False, save_weights_only=False, mode='auto', period=1)

model.save('model.h5')
