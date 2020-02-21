import tensorflow.compat.v1 as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_boston
from sklearn.utils import shuffle
from sklearn.preprocessing import scale

tf.disable_v2_behavior()

x, y = load_boston(True)
x, y = shuffle(x, y)

x_train = scale(x[:300])
x_test = scale(x[300:])

y_train = y[:300]
y_test = y[300:]

w = tf.Variable(tf.random.normal([13, 1], mean=0.0, stddev=1.0, dtype=tf.float64))
b = tf.Variable(tf.zeros(1, dtype=tf.float64))

x = tf.placeholder(tf.float64)
y = tf.placeholder(tf.float64)

pred = tf.add(b, tf.matmul(x, w))

squared_deltas = tf.square(y - pred)

loss = tf.reduce_mean(squared_deltas)

init = tf.initialize_all_variables()

optimizer = tf.train.GradientDescentOptimizer(0.0005).minimize(loss)

cost_history = []

epochs = 10000

with tf.Session() as sess:
    sess.run(init)

    for i in range(epochs):
        sess.run(optimizer, {x: x_train, y: y_train})
        if i % 10 == 0:
            cost_history.append(sess.run(loss, {x: x_train, y: y_train}))

        if i % 500 == 0:
            print(sess.run(loss, {x: x_train, y: y_train}))

    plt.plot(cost_history)
    plt.show()

    print("error on test data", sess.run(loss, {x: x_test, y: y_test}))
    sess.close()




