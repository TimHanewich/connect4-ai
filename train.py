import tensorflow as tf
import numpy
import random
import connect4
import connect4_infra

inputs:tf.keras.layers.Dense = tf.keras.layers.Input(42)
h1:tf.keras.layers.Dense = tf.keras.layers.Dense(600, "relu")
h2:tf.keras.layers.Dense = tf.keras.layers.Dense(500, "relu")
h3:tf.keras.layers.Dense = tf.keras.layers.Dense(400, "relu")
h4:tf.keras.layers.Dense = tf.keras.layers.Dense(250, "relu")
h5:tf.keras.layers.Dense = tf.keras.layers.Dense(150, "relu")
h6:tf.keras.layers.Dense = tf.keras.layers.Dense(50, "relu")
outputs:tf.keras.layers.Dense = tf.keras.layers.Dense(7)

model = tf.keras.Sequential()
model.add(inputs)
model.add(h1)
model.add(h2)
model.add(h3)
model.add(h4)
model.add(h5)
model.add(h6)
model.add(outputs)

model.compile("adam", "mean_squared_error")




        
