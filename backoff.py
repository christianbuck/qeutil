#!/usr/bin/env python

import sys
from collections import defaultdict
from itertools import imap, izip

if __name__ == "__main__":

    for linenr, line in enumerate(sys.stdin):
        if not '=' in line:
            continue
        if '</s>' in line:
            print ''
            continue
        if len(line) == 0:
            continue
        if 'logprob' in line:
            continue
        if not line.strip()[0].startswith('p('):
            pass
            #continue
        line = line.strip().split('=')[1]
        line = line.split()[0][1:-1].replace('gram','')
        print line,
