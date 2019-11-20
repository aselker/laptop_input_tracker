#!/usr/bin/env python3

import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":

    data_series = []

    for filename in sys.argv[1:]:
        series = pickle.load(open(filename, "rb"))

        first_valid = 0
        while any([x is None for x in series[first_valid]]):
            first_valid += 1

        series = series[first_valid:]

        data_series += series

    data_series = np.array(sorted(data_series))

    ts = data_series[:, 0]
    xs = data_series[:, 1]
    ys = data_series[:, 2]

    for x in xs:
        if not (0 < x < 3200):
            print(x)

    plt.plot(xs, ys)
    plt.show()
