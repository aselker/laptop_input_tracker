#!/usr/bin/env python3

import sys
import pickle

print(pickle.load(open(sys.argv[1], "rb")))
