#!/usr/bin/env python3

import sys
import pickle
import matplotlib.pyplot as plt

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

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    assert len(alphabet) == 26

    letter_1s_lower = [w for w in one_grams if w[0] in alphabet]
    letter_1s_upper = [
        w for w in one_grams if w[0].lower() in alphabet and w[0].isupper()
    ]

    print(letter_1s_lower)
    print(letter_1s_upper)

    plt.barh(range(26), letter_1s_lower)
    plt.show()
