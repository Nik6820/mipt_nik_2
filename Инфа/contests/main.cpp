#include <iostream>
#include <string>
using namespace std;

bool check_them::operator==(student& st1, student& st2) {
    return st1.id_number_string==st2.id_number_string;
}



template<typename T>
bool check_them(T& x, T& y, T& z);  

struct student {
    std::string name;
    std::string id_number_string;
};

int main()
{
    student a = {"Andy", "1234 123123"};
    student b = {"Andrew", "1234 123123"};
    student c = {"Andy", "1234123123"};
    cout << boolalpha << "Check result is: " << check_them(a, b, c) << endl;
    return 0;
}