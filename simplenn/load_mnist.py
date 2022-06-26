import six.moves.cPickle as pickle

import numpy as np

def encode_label(j):
    e = np.zeros((10, 1))
    e[j] = 1.
    return e

def _do_load_data():
    with np.load('mnist.npz') as f:
        x_train, y_train = f['x_train'], f['y_train']
        x_test, y_test = f['x_test'], f['y_test']
        return (x_train, y_train), (x_test, y_test)

def shape_data(data):
    features = [np.reshape(x, (784, 1)) for x in data[0]]
    labels = [encode_label(y) for y in data[1]]
    return list(zip(features, labels))


def load_data():
    train_data, test_data = _do_load_data()
    return shape_data(train_data), shape_data(test_data)
