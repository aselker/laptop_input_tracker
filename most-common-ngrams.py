#!/usr/bin/env python3

import sys
import pickle

ngrams = pickle.load(open(sys.argv[1], "rb"))

one_grams = [ng for ng in ngrams.items() if type(ng[0]) == str]
two_grams = [ng for ng in ngrams.items() if type(ng[0]) == tuple and len(ng[0]) == 2]
three_grams = [ng for ng in ngrams.items() if type(ng[0]) == tuple and len(ng[0]) == 3]
print(len(three_grams))

one_grams = sorted(one_grams, key=lambda x: -x[1])
two_grams = sorted(two_grams, key=lambda x: -x[1])
three_grams = sorted(three_grams, key=lambda x: -x[1])

print(one_grams[:100])
print(two_grams[:100])
print(three_grams[:100])
