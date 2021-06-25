
#title           :testKeras
#description     :TRNG
#author          :Sasha Kacanski
#date            :7/27/20
#version         :0.0.1
#usage           :
#notes           :
#python_version  :3.6.3
#==============================================================================

import numpy as np
import tensorflow as tf
##from tensorflow.keras.layers.experimental import preprocessing

data = np.array([[1,2,3,4,5], [6,7,8,9,10], [22,34,40,35,37],])
normalized_data = tf.keras.preprocessing.sequence.pad_sequences(data)
##layer.adapt(data)
##normalized_data = layer(data)

print("Features mean: %.2f" % (normalized_data.mean()))
print("Features std: %.2f" % (normalized_data.std()))

