#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from math import exp, log1p
from levenshtein import Levenshtein

# 0 ||| también aumentó en México , donde la economía se ha recuperado después de sufrir una caída en la producción del año pasado .  ||| d: 0 -3.89513 0 0 -2.79308 0 0 lm: -75.4448 w: -23 tm: -25.0151 -31.3059 -14.031 -32.8097 9.99896 ||| -9.75692

def log_add(x,y):
    if y == None:
        assert x != None
        return x
    if x == None:
        assert y != None
        return y
    return max(x, y) + log1p(exp( -abs(x - y) ));


def align_hyp(ref, hyp):
    match = []
    hyp_idx = 0
    ref_idx = 0
    lev = Levenshtein(ref, hyp)
    for i, op in enumerate(lev.editops()):
        assert hyp_idx < len(hyp) or op == Levenshtein.INS
        assert ref_idx < len(ref) or op == Levenshtein.DEL
        if op == Levenshtein.KEEP:
            assert hyp[hyp_idx] == ref[ref_idx]
            match.append(hyp[hyp_idx])
            hyp_idx += 1
            ref_idx += 1
        elif op == Levenshtein.SUB:
            match.append(None)
            hyp_idx += 1
            ref_idx += 1
        elif op == Levenshtein.DEL:
            hyp_idx += 1
        else:
            assert op == Levenshtein.INS
            match.append(None)
            ref_idx += 1
    return match


def process_buff(curr_id, buff, align):
    if not buff:
        return

    first_best = buff[0][1].split()

    p_sum = None
    p_sum_exp = 0.0

    for i in range(len(buff)):
        sent_id, hyp, score = buff[i]
        assert sent_id == curr_id
        p_sum = log_add(p_sum, score)
        p_sum_exp += exp(score)
        hyp = hyp.split()
        if align:
            hyp = align_hyp(first_best, hyp)
            assert len(hyp) == len(first_best)
        buff[i][1] = hyp


    for pos, w in enumerate(first_best):
        p_w = None
        for sent_id, hyp, score in buff:
            if pos < len(hyp) and hyp[pos] == w:
                p_w = log_add(p_w, score)
            elif align:
                assert hyp[pos] == None

        #print curr_id, pos, w, p_w, exp(p_w), p_w - p_sum, exp(p_w - p_sum)
        print p_w - p_sum,
    print ""



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-align', action='store_true', help='perform levenshtein alignment')
    args = parser.parse_args(sys.argv[1:])

    buff = []
    curr_id = 0
    for linenr, line in enumerate(sys.stdin):
        line = line.decode('utf-8').strip().split('|||')
        #print repr(line[1])

        line[0] = int(line[0])
        line[1] = u"%s" %line[1]
        line[-1] = float(line[-1])
        line.pop(2)
        # line[1] = line[1].split()
        if curr_id != line[0]:
            process_buff(curr_id, buff, align=args.align)

            buff = []
            curr_id = line[0]
        buff.append(list(line))

    process_buff(curr_id, buff, align=args.align)
