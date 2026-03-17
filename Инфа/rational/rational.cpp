#include "rational.h"
#include <numeric>   // для std::gcd
#include <cstdlib>   // для std::abs

void rational::normalize() {
    if (m == 0) {
        throw std::runtime_error("denominator cannot be zero");
    }
    // Приводим знак к числителю
    if (m < 0) {
        n = -n;
        m = -m;
    }
    // Сокращаем дробь
    int g = std::gcd(std::abs(n), m);
    if (g != 0) {
        n /= g;
        m /= g;
    }
}

rational::rational(int num, int den) : n(num), m(den) {
    normalize();
}

rational rational::operator+(const rational& other) const {
    return rational(n * other.m + other.n * m, m * other.m);
}

rational rational::operator-(const rational& other) const {
    return rational(n * other.m - other.n * m, m * other.m);
}

rational rational::operator*(const rational& other) const {
    return rational(n * other.n, m * other.m);
}

rational rational::operator/(const rational& other) const {
    if (other.n == 0) {
        throw std::runtime_error("division by zero");
    }
    return rational(n * other.m, m * other.n);
}

bool rational::operator==(const rational& other) const {
    return n == other.n && m == other.m;
}

bool rational::operator!=(const rational& other) const {
    return !(*this == other);
}

bool rational::operator<(const rational& other) const {
    return n * other.m < other.n * m;
}

bool rational::operator<=(const rational& other) const {
    return *this < other || *this == other;
}

bool rational::operator>(const rational& other) const {
    return !(*this <= other);
}

bool rational::operator>=(const rational& other) const {
    return !(*this < other);
}

std::ostream& operator<<(std::ostream& os, const rational& r) {
    if (r.m == 1) {
        os << r.n;
    } else {
        os << r.n << '/' << r.m;
    }
    return os;
}

std::istream& operator>>(std::istream& is, rational& r) {
    char slash;
    int num, den;
    if (is >> num) {
        if (is.peek() == '/') {
            is >> slash >> den;
            r = rational(num, den);
        } else {
            r = rational(num, 1);
        }
    }
    return is;
}