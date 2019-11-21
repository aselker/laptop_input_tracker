#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from skimage.filters import gaussian

from pickle_merger import import_and_merge


def show_streamlines(diffs):
    magnitude = np.transpose(np.linalg.norm(diffs, axis=2)) * 6
    # magnitude = np.clip(magnitude, None, 10)

    ys, xs = np.mgrid[0 : diffs.shape[1], 0 : diffs.shape[0]]

    xvels = np.transpose(diffs[:, :, 0])
    yvels = np.transpose(diffs[:, :, 1])

    plt.streamplot(xs, ys, xvels, yvels, linewidth=magnitude, density=3, arrowstyle="-")


def show_heatmap(diffs):
    magnitude = np.linalg.norm(diffs, axis=2)
    magnitude = np.array(gaussian(magnitude, sigma=50))

    def color_map(x):
        x = x - np.amin(x)
        x = x / np.amax(x)

        fudge_up = 0.8
        fudge_down = 1.4
        x = x * (1 + fudge_up + fudge_down)
        x = np.clip(x, 0, 1)

        start_rgb = np.array([135, 210, 206]) / 255
        end_rgb = np.array([255, 255, 255]) / 255

        background = np.array([np.full_like(magnitude, s) for s in start_rgb])
        foreground = np.array([np.full_like(magnitude, s) for s in end_rgb])

        mixed = (x * foreground) + ((1 - x) * background)

        return np.transpose(mixed)

    colors = color_map(magnitude)
    print(colors.shape)

    plt.imshow(colors)


screen_size = (3200, 1800)

if __name__ == "__main__":
    data_series = np.array(import_and_merge(sys.argv[1:]))

    poss = data_series[:, 1:3].astype(np.int32)
    diffs = np.diff(poss, axis=0)

    total_diffs = np.zeros((screen_size[0], screen_size[1], 2))

    for pos, diff in zip(poss, diffs):
        if np.linalg.norm(diff) < 50:
            total_diffs[tuple(pos)] += diff

    total_diffs = gaussian(total_diffs, sigma=20, multichannel=True)

    clip_amt = 50  # TODO: Adjust this
    total_diffs = total_diffs[clip_amt:-clip_amt, clip_amt:-clip_amt, :]

    # amplitudes = np.linalg.norm(total_diffs, axis=2)
    # sns.heatmap(amplitudes)
    # plt.show()

    plt.figure(figsize=(32, 18))
    show_streamlines(total_diffs)
    show_heatmap(total_diffs)
    # plt.savefig("streamlines.pdf")
    plt.show()
