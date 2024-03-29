#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
import pickle
from datetime import datetime

from pickle_merger import import_and_merge


def make_usage_timeseries(times):
    # first_time, last_time = min(times), max(times)
    first_time, last_time = 0, 60 * 60 * 24
    bucket_size = 60 * 60  # Seconds
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


def fudge_nonzero(yss, fudge_value=1):
    yss_fudged = yss.copy()

    for i, ys in enumerate(zip(*yss_fudged)):
        if any(ys):
            for j, y in enumerate(ys):
                if not y:
                    yss_fudged[j][i] = fudge_value

    return yss_fudged


def criscross_plot(xs, ys, fill_color, dot_color, line_color, *args, **kwargs):
    ys_1 = np.array(ys)
    ys_2 = np.array(ys)

    ys_1[::2] = 0
    ys_2[1::2] = 0

    plt.plot(xs, ys_1, color=line_color, *args, **kwargs)
    plt.plot(xs, ys_2, color=line_color, *args, **kwargs)
    plt.fill_between(xs, ys, 0, color=fill_color)
    plt.plot(xs, ys, ".", color=dot_color, *args, **kwargs)


def loop_by_day(times):
    # TODO: Offset
    wrap_time = 1575176400 + (5 * 60 * 60)  # 5am EST
    day = 60 * 60 * 24
    times = (np.asarray(times) - wrap_time) % day  #  + wrap_time
    return sorted(times)


if __name__ == "__main__":
    assert len(sys.argv) == 3

    plt.figure(figsize=(20, 8))
    # plt.axis("off")

    line_color = tuple(np.array([135, 210, 206]) / 255)
    fill_colors = [(1, 1, 1), tuple(np.array([95, 85, 110]) / 255)]

    datess, amountss = [], []
    for i, filename in enumerate(sys.argv[1:]):
        # data_series = np.array(pickle.load(open(filename, "rb")))
        data_series = np.array(import_and_merge([filename]))
        times = loop_by_day(data_series[:, 0])
        dates, amounts = make_usage_timeseries(times)

        amounts = np.array(amounts)

        datess.append(dates)
        amountss.append(amounts)

    amountss = fudge_nonzero(amountss, np.mean(amountss) / 12)
    amountss[1] = -amountss[1]  # Make one plot upside down

    for i, (dates, amounts) in enumerate(zip(datess, amountss)):
        criscross_plot(
            dates,
            amounts,
            fill_color=fill_colors[i],
            dot_color=fill_colors[-i - 1],
            line_color=line_color,
            linewidth=1.5,
            markersize=12,
        )

    # plt.savefig("mouse_timeseries.png", dpi=300, transparent=True)
    plt.savefig("mouse_timeseries.svg", transparent=True)
    # plt.show()
