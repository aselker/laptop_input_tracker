#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
import pickle
from datetime import datetime

from pickle_merger import import_and_merge


def make_usage_timeseries(times):
    first_time, last_time = min(times), max(times)
    bucket_size = 10 * 60  # Seconds
    num_buckets = (last_time - first_time) / bucket_size

    buckets = []
    i = 0
    for bucket_start in np.arange(first_time, last_time, bucket_size):
        bucket = 0
        while (i < len(times)) and (times[i] < (bucket_start + bucket_size)):
            bucket += 1
            i += 1
        buckets.append([bucket_start + bucket_size / 2, bucket])

    dates = [datetime.fromtimestamp(b[0]) for b in buckets]
    amounts = [b[1] for b in buckets]

    return dates, amounts


def criscross_plot(xs, ys, *args, **kwargs):
    ys_1 = np.array(ys)
    ys_2 = np.array(ys)

    ys_1[::2] = 0
    ys_2[1::2] = 0

    plt.plot(xs, ys, *args, **kwargs)
    plt.plot(xs, ys_1, *args, **kwargs)
    plt.plot(xs, ys_2, *args, **kwargs)


if __name__ == "__main__":
    assert len(sys.argv) == 3

    plt.figure(figsize=(60, 4))

    for i, filename in enumerate(sys.argv[1:]):
        # data_series = np.array(pickle.load(open(filename, "rb")))
        data_series = np.array(import_and_merge([filename]))
        times = data_series[:, 0]
        dates, amounts = make_usage_timeseries(times)

        amounts = np.array(amounts)
        if i % 2:
            amounts = -amounts

        criscross_plot(dates, amounts, "g" if i else "b", linewidth=0.6)

    plt.savefig("mouse_timeseries.png")
