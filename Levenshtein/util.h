#ifndef UTIL_H_
#define UTIL_H_

#include <sstream>
#include <iostream>
#include <vector>

using namespace std;

void usage(void **argtable, const char *progname) {
  FILE *fp = stdout;
  fprintf(fp, "Usage: %s ", progname);
  arg_print_syntaxv(fp, argtable, "\n");
  arg_print_glossary(fp, argtable, " %-50s %s\n");
}

template<class T>
inline string to_string(const T& t) {
  stringstream ss;
  ss << t;
  return ss.str();
}

void progress(const size_t iter, const size_t corpus_size, const size_t speed, const bool force = false) {
  const size_t true_iter = iter % corpus_size;
  if (true_iter > 0 && true_iter % speed == 0) {
    cerr << ".";
    cerr.flush();
  }

  if ((true_iter > 0 && true_iter % (50 * speed) == 0) != (force)) {
    cerr << "[" << iter % corpus_size << "]" << endl;
    cerr.flush();
  }
}

template<class T>
void printVector(const vector<T>& v, const double threshold = 0.5, const bool verbose = false) {
  for (size_t i = 0; i < v.size(); ++i) {
    if (i > 0) {
      cout << " ";
    }
    cout << (v.at(i) > threshold);
    if (verbose)
      cout << " (" << v.at(i) << ")";
  }
  cout << endl;
}

// from: http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#C.2B.2B
template<class T>
unsigned int levenshtein_distance(const T &s1, const T & s2) {
  const size_t len1 = s1.size(), len2 = s2.size();
  vector<unsigned int> col(len2 + 1), prevCol(len2 + 1);

  for (unsigned int i = 0; i < prevCol.size(); i++)
    prevCol[i] = i;
  for (unsigned int i = 0; i < len1; i++) {
    col[0] = i + 1;
    for (unsigned int j = 0; j < len2; j++)
      col[j + 1] = min(min(1 + col[j], 1 + prevCol[1 + j]),
          prevCol[j] + (s1[i] == s2[j] ? 0 : 1));
    col.swap(prevCol);
  }
  return prevCol[len2];
}

template<class T>
unsigned int OptimalStringAlignmentDistance(const T &s1, const T & s2) {
  const size_t len1 = s1.size(), len2 = s2.size();
  vector<unsigned int> col(len2 + 1), prevCol(len2 + 1);

  for (unsigned int i = 0; i < prevCol.size(); i++)
    prevCol[i] = i;
  for (unsigned int i = 0; i < len1; i++) {
    col[0] = i + 1;
    for (unsigned int j = 0; j < len2; j++) {
      col[j + 1] = min(min(1 + col[j], 1 + prevCol[1 + j]),
          prevCol[j] + (s1[i] == s2[j] ? 0 : 1));
      if (i > 0 && j > 0 && s1[i] == s2[j-1] && s1[i-1] == s2[j]) {
      }
    }
    col.swap(prevCol);
  }
  return prevCol[len2];
}

#endif /* UTIL_H_ */
