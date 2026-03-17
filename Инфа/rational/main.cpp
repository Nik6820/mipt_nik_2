#include <iostream>
#include <fstream>
#include <iomanip>
#include "rational.h"

int main() {
    const std::string input_filename = "input.txt";
    const std::string output_filename = "output.txt";

    std::ifstream in(input_filename);
    if (!in.is_open()) {
        std::cerr << "Error: cannot open input file " << input_filename << std::endl;
        return 1;
    }

    const int count = 5;
    rational numbers[count];  

    // Читаем 5 рациональных чисел
    for (int i = 0; i < count; ++i) {
        if (!(in >> numbers[i])) {
            std::cerr << "Error: failed to read rational number #" << i+1 << std::endl;
            return 1;
        }
    }

    in.close();

    // Умножаем каждое число на 3
    for (int i = 0; i < count; ++i) {
        numbers[i] = numbers[i] * rational(3);
    }

    std::ofstream out(output_filename);
    if (!out.is_open()) {
        std::cerr << "Error: cannot open output file " << output_filename << std::endl;
        return 1;
    }

    // Выводим с точностью до двух знаков после запятой
    out << std::fixed << std::setprecision(2);
    for (int i = 0; i < count; ++i) {
        double val = static_cast<double>(numbers[i].getn()) / numbers[i].getm();
        out << val << std::endl;
    }

    out.close();
    std::cout << "Results written to " << output_filename << std::endl;

    return 0;
}