#!/usr/bin/env python3

import sys
import pickle

if __name__ == "__main__":

    history_1 = pickle.load(open(sys.argv[1], "rb"))
    history_2 = pickle.load(open(sys.argv[2], "rb"))

    for key, value in history_1.items():
        history_2[key] = history_2.get(key, 0) + value

    pickle.dump(history_2, open(sys.argv[3], "wb"))
