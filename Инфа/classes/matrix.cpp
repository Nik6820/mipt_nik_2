#include <iostream>
#include <cmath>

// -------------------- Класс Matrix --------------------
class Matrix {
private:
    double** data;
    int rows_, cols_;

    // Вспомогательная функция для выделения памяти
    void allocate(int rows, int cols) {
        data = new double*[rows];
        for (int i = 0; i < rows; i++) {
            data[i] = new double[cols];
            for (int j = 0; j < cols; j++) data[i][j] = 0.0;
        }
    }

    // Вспомогательная функция для освобождения памяти
    void deallocate() {
        if (data) {
            for (int i = 0; i < rows_; i++) delete[] data[i];
            delete[] data;
        }
    }

public:
    // Конструкторы
    Matrix() : data(nullptr), rows_(0), cols_(0) {}
    
    Matrix(int rows, int cols) : rows_(rows), cols_(cols) {
        allocate(rows, cols);
    }
    
    Matrix(std::initializer_list<std::initializer_list<double>> list) {
        rows_ = list.size();
        cols_ = (rows_ == 0) ? 0 : list.begin()->size();
        allocate(rows_, cols_);
        
        int i = 0;
        for (auto row : list) {
            int j = 0;
            for (double val : row) data[i][j++] = val;
            i++;
        }
    }
    
    // Копирующий конструктор
    Matrix(const Matrix& other) : rows_(other.rows_), cols_(other.cols_) {
        allocate(rows_, cols_);
        for (int i = 0; i < rows_; i++)
            for (int j = 0; j < cols_; j++)
                data[i][j] = other.data[i][j];
    }
    
    // Деструктор
    ~Matrix() {
        deallocate();
    }
    
    // Оператор присваивания
    Matrix& operator=(const Matrix& other) {
        if (this != &other) {
            deallocate();
            rows_ = other.rows_;
            cols_ = other.cols_;
            allocate(rows_, cols_);
            for (int i = 0; i < rows_; i++)
                for (int j = 0; j < cols_; j++)
                    data[i][j] = other.data[i][j];
        }
        return *this;
    }

    // Геттеры
    int rows() const { return rows_; }
    int cols() const { return cols_; }

    // Доступ к элементам
    double& operator()(int i, int j) { return data[i][j]; }
    const double& operator()(int i, int j) const { return data[i][j]; }

    // Транспонирование матрицы
    Matrix transpose() const {
        Matrix result(cols_, rows_);  // меняем размеры местами
        for (int i = 0; i < rows_; i++)
            for (int j = 0; j < cols_; j++)
                result(j, i) = data[i][j];  // элемент (i,j) становится (j,i)
        return result;
    }

    // Сложение матриц
    Matrix operator+(const Matrix& other) const {
        if (rows_ != other.rows_ || cols_ != other.cols_) return Matrix();
        Matrix result(rows_, cols_);
        for (int i = 0; i < rows_; i++)
            for (int j = 0; j < cols_; j++)
                result(i, j) = data[i][j] + other.data[i][j];
        return result;
    }

    // Умножение матриц
    Matrix operator*(const Matrix& other) const {
        if (cols_ != other.rows_) return Matrix();
        Matrix result(rows_, other.cols_);
        for (int i = 0; i < rows_; i++) {
            for (int k = 0; k < cols_; k++) {
                double aik = data[i][k];
                if (aik != 0.0) {
                    for (int j = 0; j < other.cols_; j++)
                        result(i, j) += aik * other.data[k][j];
                }
            }
        }
        return result;
    }

    // Умножение на скаляр
    Matrix operator*(double scalar) const {
        Matrix result(rows_, cols_);
        for (int i = 0; i < rows_; i++)
            for (int j = 0; j < cols_; j++)
                result(i, j) = data[i][j] * scalar;
        return result;
    }

    // Определитель
    double determinant() const {
        if (rows_ != cols_ || rows_ == 0) return 0;
        int n = rows_;
        
        Matrix A(*this);
        double det = 1.0;
        int sign = 1;

        for (int i = 0; i < n; i++) {
            int pivot = i;
            for (int k = i + 1; k < n; k++) {
                if (std::abs(A(k, i)) > std::abs(A(pivot, i)))
                    pivot = k;
            }
            if (std::abs(A(pivot, i)) < 1e-12) return 0.0;
            
            if (pivot != i) {
                double* temp = A.data[i];
                A.data[i] = A.data[pivot];
                A.data[pivot] = temp;
                sign = -sign;
            }
            
            for (int k = i + 1; k < n; k++) {
                double factor = A(k, i) / A(i, i);
                if (factor != 0.0) {
                    for (int j = i; j < n; j++) {
                        A(k, j) -= factor * A(i, j);
                    }
                }
            }
            det *= A(i, i);
        }
        return sign * det;
    }

    // Ранг матрицы
    int rank() const {
        Matrix A(*this);
        int r = 0;
        int m = rows_;
        int n = cols_;

        for (int col = 0, row = 0; col < n && row < m; col++) {
            int sel = -1;
            for (int i = row; i < m; i++) {
                if (std::abs(A(i, col)) > 1e-12) {
                    sel = i;
                    break;
                }
            }
            if (sel == -1) continue;

            if (sel != row) {
                double* temp = A.data[row];
                A.data[row] = A.data[sel];
                A.data[sel] = temp;
            }

            for (int i = row + 1; i < m; i++) {
                double factor = A(i, col) / A(row, col);
                if (factor != 0.0) {
                    for (int j = col; j < n; j++) {
                        A(i, j) -= factor * A(row, j);
                    }
                }
            }
            row++;
            r++;
        }
        return r;
    }

    // Оператор вывода
    friend std::ostream& operator<<(std::ostream& os, const Matrix& M) {
        for (int i = 0; i < M.rows_; i++) {
            os << "[ ";
            for (int j = 0; j < M.cols_; j++) {
                os << M(i, j) << (j + 1 < M.cols_ ? ", " : " ");
            }
            os << "]\n";
        }
        return os;
    }
};

// Умножение скаляра на матрицу
Matrix operator*(double scalar, const Matrix& M) {
    return M * scalar;
}

// -------------------- Пример использования --------------------
int main() {
    Matrix A = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };
    
    std::cout << "Исходная матрица A:\n" << A;
    std::cout << "Транспонированная A^T:\n" << A.transpose();
    
    
    Matrix B = {
        {1, 2},
        {3, 4},
        {5, 6}
    };
    
    std::cout << "\nМатрица B (3x2):\n" << B;
    std::cout << "Транспонированная B^T (2x3):\n" << B.transpose();
    
    // Демонстрация остальных методов
    Matrix C = {
        {2, -1, 0},
        {-1, 2, -1},
        {0, -1, 2}
    };
    std::cout << "\nМатрица C:\n" << C;
    std::cout << "det(C) = " << C.determinant() << std::endl;
    
    Matrix D = {
        {1, 2, 3},
        {2, 4, 6},
        {3, 6, 9}
    };
    std::cout << "\nМатрица D:\n" << D;
    std::cout << "\nC + D =\n" << C + D << std::endl;
    Matrix E = {
        {1, 2, 3},
        {4, 5, 6}
    };
    Matrix F = {
        {7, 8},
        {9, 10},
        {11, 12}
    };
    std::cout << "\nМатрица E (2x3):\n" << E;
    std::cout << "Матрица F (3x2):\n" << F;
    std::cout << "E * F =\n" << E * F;
    
    return 0;
}