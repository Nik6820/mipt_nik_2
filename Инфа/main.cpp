#include <iostream>
#include <map>
#include <string>

using namespace std;

map<char, int> counter(const string& word) {
    map<char, int> charCount;
    for (char c : word) {
        charCount[c]++;
    }
    return charCount;
}

bool isAnagram(const string& word1, const string& word2) {

    map<char, int> count1 = counter(word1);
    map<char, int> count2 = counter(word2);
    
    return count1 == count2;
}

int main() {
    int N;
    cout << "Введите количество пар слов: ";
    cin >> N;
    
    for (int i = 0; i < N; i++) {
        string word1, word2;
        
        cout << "Введите пару слов " << i + 1 << ": ";
        cin >> word1 >> word2;
        
        if (isAnagram(word1, word2)) {
            cout << "YES" << endl;
        } else {
            cout << "NO" << endl;
        }
    }
    
    return 0;
}