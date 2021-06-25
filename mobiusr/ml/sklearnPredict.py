import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import tensorflow as tf


points = 5 # number of data points to generate
timesteps = 5 # number of time steps per sample as LSTM layers need input shape (samples, time steps, features)
features = 1 # number of features per time step as LSTM layers need input shape (samples, time steps, features)

x = np.arange(points + 1) # array([1,2,3,4,5])
y = x[1:]
x = x[:5]


dataset = np.hstack((x.reshape((points, 1)),y.reshape((points, 1))))
scaler = MinMaxScaler((0, 1))
scaled = scaler.fit_transform(dataset)

x_train = scaled[:,0] # first column
x_train = x_train.reshape((points // timesteps, timesteps, features)) # as i stated before LSTM layers need input shape (samples, time steps, features)

y_train = scaled[:,1] # second column
y_train = y_train[2::3]

regresor = tf.keras.models.Sequential()
regresor.add(tf.keras.layers.LSTM(units = 4, return_sequences = True))
regresor.add(tf.keras.layers.LSTM(units = 2))
regresor.add(tf.keras.layers.Dense(units = 1))
regresor.compile(optimizer = 'rmsprop', loss = 'mse')
regresor.fit(x_train, y_train, batch_size = 2, epochs = 500, verbose = 1)
y_hats = regresor.predict(x_train)
print(y_hats)



