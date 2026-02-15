#include "iostream"
using namespace std;

class Animal {
public:
    virtual string getType() = 0;
    virtual bool isDangerous() = 0;
};

class ZooKeeper {
public:
    int count = 0;
    // Создаём смотрителя зоопарка
    ZooKeeper() {
        
    }

    // Смотрителя попросили обработать очередного зверя.
    // Если зверь был опасный, смотритель фиксирует у себя этот факт.
    void handleAnimal(Animal* a){
        count+=a->isDangerous();
    }

    // Возвращает, сколько опасных зверей было обработано на данный момент.
    int getDangerousCount(){
        return count;
    }
};

int main(){
    ZooKeeper z;
    Monkey *m = new Monkey();
    z.handleAnimal(m);
    delete m;
    m = new Monkey();
    z.handleAnimal(m);
    delete m;
    Lion *l = new Lion();
    z.handleAnimal(l);
    delete l;
    cout << z.getDangerousCount() << endl;
}