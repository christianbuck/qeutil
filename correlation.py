#!/usr/bin/env python

import math
import sys
import scipy.stats

def average(x):
    assert len(x) > 0
    return float(sum(x)) / len(x)

def pearson_def(x, y):
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    avg_x = average(x)
    avg_y = average(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    for idx in range(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y
        diffprod += xdiff * ydiff
        xdiff2 += xdiff * xdiff
        ydiff2 += ydiff * ydiff

    return diffprod / math.sqrt(xdiff2 * ydiff2)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', action='store', type=int, help="use only first n lines",
                        default=1832)
    parser.add_argument('-pearson', action='store_true', help="pearson's correlation coefficient")
    parser.add_argument('-spearman', action='store_true', help="spearman's rank correlation coefficient")
    parser.add_argument('-q', action='store_true', help="surpress notifications")
    parser.add_argument('-pval', action='store_true', help="print p-values")

    args = parser.parse_args(sys.argv[1:])

    x,y = [], []
    for linenr, line in enumerate(sys.stdin):
        if linenr >= args.n:
            if not args.q:
                print "skipping lines after %s" %(args.n)
            break
        line = map(float, line.split())
        if len(line) != 2:
            print "weird line:", line
        x.append(line[0])
        y.append(line[1])

    if args.pearson:
        pearsons_r, p_value = scipy.stats.stats.pearsonr(x, y)
        print pearsons_r
        if args.pval:
            print p_value
    if args.spearman:
        spearmans_r, p_value = scipy.stats.stats.spearmanr(x, y)
        print spearmans_r
        if args.pval:
            print p_value
    #try:
    #    print pearson_def(x, y)
    #    print "scipy pearson", scipy.stats.stats.pearsonr(x, y)[0]
    #    print "scipy spearman", scipy.stats.stats.spearmanr(x, y)[0]
    #
    #except ZeroDivisionError:
    #    print "NaN"
