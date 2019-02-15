from .Better import bet_test
from .fpgrouth import fp_test
import time

methods = [bet_test, fp_test]
paths = [r'/Users/hushichang/Downloads/pumsb.dat']
minSups = [0.2, 0.3, 0.4]

for path in paths:
    for minSup in minSups:
        for method in methods:
            start = time.time()
            method(path, minSup)


