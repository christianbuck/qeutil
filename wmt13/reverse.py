#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if __name__ == "__main__":

    for linenr, line in enumerate(sys.stdin):
        line = line.decode('utf-8').strip().split()
        line.reverse()
        sys.stdout.write(u" ".join(line).encode('utf-8'))
