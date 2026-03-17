#pragma once

#include <iostream>
#include <stdexcept>

class rational {
private:
    int n;   // числитель
    int m;   // знаменатель

    void normalize();   // нормализация и сокращение дроби

public:
    rational(int num = 0, int den = 1);

    rational operator+(const rational& other) const;
    rational operator-(const rational& other) const;
    rational operator*(const rational& other) const;
    rational operator/(const rational& other) const;

    bool operator==(const rational& other) const;
    bool operator!=(const rational& other) const;
    bool operator<(const rational& other) const;
    bool operator<=(const rational& other) const;
    bool operator>(const rational& other) const;
    bool operator>=(const rational& other) const;

    friend std::ostream& operator<<(std::ostream& os, const rational& r);
    friend std::istream& operator>>(std::istream& is, rational& r);

    int getn() const { return n; }
    int getm() const { return m; }
};