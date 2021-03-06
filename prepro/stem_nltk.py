#!/usr/bin/env python
import sys
import codecs
from nltk import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer

if __name__ == "__main__":
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    #sys.stdin = codecs.getreader('utf-8')(sys.stdin)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('language', help='language for snowball stemmer')
    args = parser.parse_args(sys.argv[1:])

    language = args.language.lower()
    assert language in SnowballStemmer.languages or language == 'english', "invalid language"
    stemmer = LancasterStemmer() if language == 'english' else SnowballStemmer(language)

    for line in iter(sys.stdin.readline, ''):
        words = line.decode('utf-8').split()
        stemmed_words = []
        for w in words:
            stem = "STEM"
            try:
                stem = stemmer.stem(w)
            except:
                pass
            stemmed_words.append(stem)
        sys.stdout.write("%s\n" %(u" ".join(stemmed_words)))
