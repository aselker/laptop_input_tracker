#!/usr/bin/env python3

import sys
import pickle


def import_and_merge(filenames):
    all_series = []
    for filename in filenames:
        series = pickle.load(open(filename, "rb"))

        first_valid = 0
        while any([x is None for x in series[first_valid]]):
            first_valid += 1

        series = series[first_valid:]
        all_series += series

    return sorted(all_series)


if __name__ == "__main__":
    input_filenames = sys.argv[1:-1]
    output_filename = sys.argv[-1]

    pickle.dump(import_and_merge(input_filenames), open(output_filename, "wb"))
