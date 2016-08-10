#include <fstream>
#include <iostream>
#include <string>
#include <unordered_set>
#include <list>

using namespace std;

unordered_set<string> dict;

bool compare_strlen (const string& first, const std::string& second) {
  return (first.length() > second.length());
}

// Checks if word is compound.
// @param[in] word  String to be checked.
// @param[in] can_match_full_word  True if this should return true when the full word is found.
// @return    true if word is compound.
bool is_word_compound(const string& word, bool can_match_full_word) {
	//if (!can_match_full_word) cout << "Checking word: " << word << endl;

	for (int len = 1; len <= word.length(); len++) {
		auto it = dict.find(word.substr(0, len));
		if (it != dict.end()) {
			if (len == word.length()) {
				return can_match_full_word;
			} else if (is_word_compound(word.substr(len, word.length()-len), true)) {
				//cout << "   compound: " << word << endl;
				return true;
			}
		}
	}
	return false;
}

int main(int argc, char *argv[]) {

	if (argc != 2) {
		cout << "Provide input file parameter." << endl;
		exit(1);
	}

	string word;
	list<string> words_by_len;

	// Read words from input file.
	ifstream infile(argv[1]);
	while (infile >> word) {
		dict.insert(word);
		words_by_len.push_back(word);
	}
	words_by_len.sort(compare_strlen);

	// Find longest compound word.
	for (auto it = words_by_len.begin(); it != words_by_len.end(); ++it) {
		if (is_word_compound(*it, false)) {
			cout << "Longest compound word is: " << *it << endl;
			return 0;
		}
	}

    cout << "No compound word found." << endl;
    return 1;
}
