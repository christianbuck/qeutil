#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from math import exp, log1p
from levenshtein import Levenshtein
# 0 ||| también aumentó en México , donde la economía se ha recuperado después de sufrir una caída en la producción del año pasado .  ||| d: 0 -3.89513 0 0 -2.79308 0 0 lm: -75.4448 w: -23 tm: -25.0151 -31.3059 -14.031 -32.8097 9.99896 ||| -9.75692


def smart_open(filename):
    if not filename:
        return None
    if filename.endswith('.gz'):
        import gzip, io
        return io.BufferedReader(gzip.open(filename))
    return open(filename)

class WPP(object):
    def log_add(self, x,y):
        if y == None:
            assert x != None
            return x
        if x == None:
            assert y != None
            return y
        return max(x, y) + log1p(exp( -abs(x - y) ));


    def align_hyp(self, ref, hyp):
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


    def process_buff(self, curr_id, buff, winning_hyp, align):
        res = []
        if not buff:
            return res

        first_best_id, first_best = winning_hyp
        assert first_best_id == curr_id

        p_sum = None
        p_sum_exp = 0.0

        for i in range(len(buff)):
            sent_id, hyp, score = buff[i]
            assert sent_id == curr_id
            p_sum = self.log_add(p_sum, score)
            p_sum_exp += exp(score)
            hyp = hyp.split()
            if align:
                hyp = self.align_hyp(first_best, hyp)
                assert len(hyp) == len(first_best)
            buff[i][1] = hyp


        for pos, w in enumerate(first_best):
            p_w = None
            for sent_id, hyp, score in buff:
                if pos < len(hyp) and hyp[pos] == w:
                    p_w = self.log_add(p_w, score)
                elif align:
                    assert hyp[pos] == None

            #print curr_id, pos, w, p_w, exp(p_w), p_w - p_sum, exp(p_w - p_sum)
            if p_w == None:
                res.append(-100.)
            else:
                res.append(p_w - p_sum)
        return res



if __name__ == "__main__":
    """ default mode is to read an nbest list as produced by moses and print
        logprobs for each word in the first-best line
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-align', action='store_true', help='perform levenshtein alignment')
    parser.add_argument('-firstbest', help='firstbest translations, one per line')
    parser.add_argument('-n', help='limit n-best entries to this many', type=int)

    args = parser.parse_args(sys.argv[1:])

    wpp = WPP()
    buff = []
    curr_id = None

    first_best = []
    if args.firstbest:
        first_best = [(linenr, line.decode('utf-8').strip().split()) \
            for linenr, line in enumerate(open(args.firstbest))]

    for linenr, line in enumerate(sys.stdin):
        line = line.decode('utf-8').strip().split('|||')
        #print repr(line[1])

        line[0] = int(line[0])
        line[1] = u"%s" %line[1]
        line[-1] = float(line[-1])
        line.pop(2)
        # line[1] = line[1].split()
        if curr_id == None or curr_id != line[0]:
            if curr_id != None:
                assert not first_best or curr_id < len(first_best)
                fb = None if not first_best else first_best[curr_id]
                if args.n and len(buff) > args.n:
                    buff = buff[:args.n]
                res = wpp.process_buff(curr_id, buff, fb, align=args.align)
                print " ".join(map(str, res))

            buff = []
            curr_id = line[0]
        buff.append(list(line))

    res = wpp.process_buff(curr_id, buff, align=args.align)
    print " ".join(map(str, res))