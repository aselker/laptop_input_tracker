#!/usr/bin/env python3

import sys
import pickle
import matplotlib.pyplot as plt

alphabet = "abcdefghijklmnopqrstuvwxyz"
assert len(alphabet) == 26


def is_letter(l):
    return l and (l.lower() in alphabet)


if __name__ == "__main__":
    ngrams = pickle.load(open(sys.argv[1], "rb"))

    one_grams = [ng for ng in ngrams.items() if type(ng[0]) == str]
    two_grams = [
        ng for ng in ngrams.items() if type(ng[0]) == tuple and len(ng[0]) == 2
    ]
    three_grams = [
        ng for ng in ngrams.items() if type(ng[0]) == tuple and len(ng[0]) == 3
    ]

    one_grams = sorted(one_grams, key=lambda x: -x[1])
    two_grams = sorted(two_grams, key=lambda x: -x[1])
    three_grams = sorted(three_grams, key=lambda x: -x[1])

    letter_1s_lower = [w for w in one_grams if is_letter(w[0]) and w[0].islower()]
    letter_1s_upper = [w for w in one_grams if is_letter(w[0]) and w[0].isupper()]

    y_pos = range(26, 0, -1)
    right_bars = [l[1] for l in letter_1s_lower]
    left_bars = [-ngrams.get(r[0].upper(), 0) for r in letter_1s_lower]

    plt.rcdefaults()
    fig, ax = plt.subplots()

    # ax.barh(range(26, 0, -1), [l[1] for l in letter_1s_lower])
    ax.barh(y_pos, right_bars)
    ax.barh(y_pos, left_bars)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([l[0] for l in letter_1s_lower])

    plt.savefig("letter_freqs.pdf")
