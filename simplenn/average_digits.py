#!/usr/bin/env python3

import numpy as np

from matplotlib import pyplot as plt

from simplenn.load_mnist import load_data
from simplenn.layers import sigmoid_double


def average_digit(data, digit):
    filtered_data = [x[0] for x in data if np.argmax(x[1]) == digit]
    filtered_array = np.asarray(filtered_data)
    return np.average(filtered_array, axis=0)

def predict(x, W, b):
    return sigmoid_double(np.dot(W, x) + b)

train, test = load_data()
avg_eight = average_digit(train, 8)

img = np.reshape(avg_eight, (28, 28))
plt.imshow(img)
plt.show()

x_3 = train[2][0]
x_18 = train[17][0]

W = np.transpose(avg_eight)
print('3 vs avg', np.dot(W, x_3))
print('18 vs avg', np.dot(W, x_18))

b = -30459.

print(predict(x_3, W, b))
print(predict(x_18, W, b))
