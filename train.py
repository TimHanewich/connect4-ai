import tensorflow as tf
import numpy
import random
import connect4
import training_tools

inputs:tf.keras.layers.Dense = tf.keras.layers.Input(42, kernel_initializer="random_uniform")
h1:tf.keras.layers.Dense = tf.keras.layers.Dense(600, "relu", kernel_initializer="random_uniform")
h2:tf.keras.layers.Dense = tf.keras.layers.Dense(500, "relu", kernel_initializer="random_uniform")
h3:tf.keras.layers.Dense = tf.keras.layers.Dense(400, "relu", kernel_initializer="random_uniform")
h4:tf.keras.layers.Dense = tf.keras.layers.Dense(250, "relu", kernel_initializer="random_uniform")
h5:tf.keras.layers.Dense = tf.keras.layers.Dense(150, "relu", kernel_initializer="random_uniform")
h6:tf.keras.layers.Dense = tf.keras.layers.Dense(50, "relu", kernel_initializer="random_uniform")
outputs:tf.keras.layers.Dense = tf.keras.layers.Dense(7, kernel_initializer="random_uniform")

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




        
