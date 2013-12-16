#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <cassert>
#include <argtable2.h>

#include <argtable2.h>
#include "util.h"

using namespace std;

class Sentence {
public:
  vector<string> words;
  vector<unsigned char> chars;

  bool empty() {
    return words.empty() && chars.empty();
  }
};

typedef vector<Sentence> document;

void readFile(const string& filename, const int max_lines, const bool charbased, document& content) {
  ifstream infile(filename.c_str());
  int linenr = 0;
  if (infile.is_open()) {
    while (infile.good() && (max_lines == 0 || max_lines > linenr)) {
      string line;
      Sentence snt;

      getline(infile, line);
      if (charbased) {
        snt.chars.assign(line.begin(), line.end());
      } else {
        string word;
        istringstream iss(line);
        while (getline(iss, word, ' ')) {
          if (word.length() > 0) {
            snt.words.push_back(word);
          }
        }
      }
      content.push_back(snt);
      linenr++;
    }

    if (content[content.size()-1].empty()) {
      content.pop_back();
    }

    infile.close();
  } else {
    cerr << "Unable to open file" << filename << endl;
  }
  cerr << "loaded " << content.size() << " lines from " << filename << endl;
}

unsigned int dist(const Sentence& s1, const Sentence& s2, const bool charbased) {
  if (charbased) {
    return levenshtein_distance(s1.chars, s2.chars);
  } else {
    return levenshtein_distance(s1.words, s2.words);
  }
}

int main(int argc, char**argv) {
  const char *progname = "train";
  struct arg_file *Af = arg_file1(NULL, NULL, "<sourcefile>", "input file (source corpus)");
  struct arg_file *Ac = arg_file1(NULL, NULL, "<corpusfile>", "hyps");
  struct arg_lit *Ahelp = arg_lit0("h", "help", "show help and exit");
  struct arg_lit *Aforce = arg_lit0("f", "force", "force full matrix");
  struct arg_lit *Astring = arg_lit0("s", "string", "string instead of word based distance");
  struct arg_int *Amax = arg_int0("m", "max-lines", "<n>", "maximum number of lines to read");
  Amax->ival[0]=0;

  struct arg_end *Aend = arg_end(20);

  void *argtable[] = { Af, Ac, Ahelp, Aforce, Astring, Amax, Aend };
  int nerrors = arg_parse(argc, argv, argtable);
  // special flags
  if (Ahelp->count > 0) {
    usage(argtable, progname);
    exit(0);
  }
  if (nerrors > 0) {
    arg_print_errors(stderr, Aend, progname);
    fprintf(stderr, "Try '%s --help' for more information.\n", progname);
    exit(EXIT_FAILURE);
  }

  const bool charbased = (Astring->count > 0);
  document data1;
  const string corpus_filename = string(Af->filename[0]);
  readFile(corpus_filename, Amax->ival[0], charbased, data1);

  document data2;
  const string reference_filename = string(Ac->filename[0]);
  if (reference_filename != corpus_filename || Aforce->count > 0) {
    cerr << "full matrix mode, reading references from " << reference_filename << "." << endl;
    readFile(Ac->filename[0], Amax->ival[0], charbased, data2);

    for (document::const_iterator cit1=data1.begin(); cit1 != data1.end(); ++cit1) {
      for (document::const_iterator cit2=data2.begin(); cit2 != data2.end(); ++cit2) {
        const unsigned int d = dist(*cit1, *cit2, charbased);
        cout << d << " ";
      }
      cout << endl;
    }
  } else {
    cerr << "computing upper triangular matrix." << endl;
    for (document::const_iterator cit1=data1.begin(); cit1 != data1.end(); ++cit1) {
      for (document::const_iterator cit2=cit1; cit2 != data1.end(); ++cit2) {
        const unsigned int d = dist(*cit1, *cit2, charbased);
        cout << d << " ";
      }
      cout << endl;
    }
  }

  return 0;
}
