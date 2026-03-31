#include <iostream>
#include <map>
#include <string>
#include <vector>

using namespace std;


template<typename T>
bool f1 ( vector<T> vec, T element) {
    for (auto elem : vec) {
        if (elem == element) {
            return true;
        }
    }
    return false;
}

template<typename K, typename T>
bool f1 (map<K, T> mp, T element) {
    for (auto elem : mp) {
        if (elem.second == element) {
            return true;
        }
    }
    return false;
}

template<typename T>
bool f2 ( vector<T> vec, T element) {
    int counter = 0;
    for (auto elem : vec) {
        if (elem == element) {
            counter++;
        }
    }
    if (counter%2 == 0) {
        return true;
    }
    return false;
}

template<typename K, typename T>
bool f2 ( map<K, T> mp, T element) {
    int counter = 0;
    for (auto elem : mp) {
        if (elem.second == element) {
            counter++;
        }
    }
    if (counter%2 == 0) {
        return true;
    }
    return false;
}

class checker {
public:
	int counter = 0;

	checker(){};

    template<class Func, class Cont, class Elem>
	void check(Func foo, vector<Cont> containers, Elem element) {
	    for (auto container : containers) {
            if (foo(container, element)) {
                counter++;
            }
	    }
	}

	~checker() {
		cout << "Counter: " << counter << endl;
	}
};


int main() {
    checker ch;

    vector<int> v1 = {1, 2, 3, 1};
    vector<int> v2 = {4, 5, 4, 4};
    vector<int> v3 = {6, 7, 8};

    map<string, int> m1 = {{"a", 1}, {"b", 2}};
    map<string, int> m2 = {{"c", 3}};
    map<string, int> m3 = {{"d", 3}, {"e", 5}, {"f", 6}};

    vector<vector<int>> vec_of_vecs = {v1, v2, v3};
    vector<map<string, int>> vec_of_maps = {m1, m2, m3};

    ch.check(f1<int>, vec_of_vecs, 4);
    ch.check(f1<string, int>, vec_of_maps, 2);
    ch.check(f2<int>, vec_of_vecs, 1);
    ch.check(f2<string, int>, vec_of_maps, 3);

    return 0;

}   