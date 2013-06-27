#!/usr/bin/env python
import sys
from math import exp


def prod(l):
    assert len(l)>0, "empty list has not product"
    p = l[0]
    for x in l[1:]:
        p *= x
    return p


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-offset', type=int, dest='offset')
    parser.add_argument('-log', action='store_true', dest='log',
                        help='treat input as log-probs', default=False)
    args = parser.parse_args(sys.argv[1:])

    for linenr, line in enumerate(sys.stdin):
        line = map(float, line.split())

        if args.log:
            line = map(exp, line)

        #if len(sys.argv)>1:
        #    offset = float(sys.argv[1])
        #    line = [max(1.0, x+offset) for x in line]

        if len(sys.argv)>2:
            # normalize
            s = sum(line)
            line = [x/s for x in line]

        print prod(line)**(1./len(line))
