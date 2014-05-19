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
    parser.add_argument('-normalize', action='store_true')
    parser.add_argument('-log', action='store_true', dest='log',
                        help='treat input as log-probs', default=False)
    parser.add_argument('-clip_min', type=float, help='minimal value')
    args = parser.parse_args(sys.argv[1:])

    for linenr, line in enumerate(sys.stdin):
        line = map(float, line.split())

        #print line
        if args.clip_min:
            line = [max(x,args.clip_min) for x in line]
        #print "clipped: ", line

        if args.log:
            line = map(exp, line)

        #if len(sys.argv)>1:
        #    offset = float(sys.argv[1])
        #    line = [max(1.0, x+offset) for x in line]

        if args.normalize:
            s = sum(line)
            line = [x/s for x in line]

        print prod(line)**(1./len(line))
