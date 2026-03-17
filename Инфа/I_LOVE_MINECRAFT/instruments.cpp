
#include <iostream>
#include <string>

using namespace std;

// Базовый класс для всех инструментов
class Tool {
protected:
    int durability;        // текущая прочность
    int maxDurability;     // максимальная прочность
    string material;       // материал (дерево, камень, железо, алмаз)
    string name;           // имя инструмента
    int damage;            // урон (для оружия)
    int miningSpeed;       // скорость копания

public:
    // Конструктор по умолчанию
    Tool() : durability(0), maxDurability(0), material("unknown"), name("unknown"), damage(0), miningSpeed(0) {
        cout << "An empty tool is created" << endl;
    }

    // Конструктор с параметрами
    Tool(int durability_, int maxDurability_, string material_, string name_, int damage_, int miningSpeed_)
        : durability(durability_), maxDurability(maxDurability_), material(material_), name(name_), damage(damage_), miningSpeed(miningSpeed_) {
        cout << "The " << name << " is crafted from " << material << endl;
    }

    // Виртуальный деструктор
    virtual ~Tool() {}

    // Использование инструмента (общее поведение)
    virtual void use() {
        if (durability <= 0) {
            cout << "The " << name << " is already broken!" << endl;
            return;
        }
        durability--;
        cout << "Using the " << name << ". Durability left: " << durability << "/" << maxDurability << endl;
        if (durability <= 0) {
            onBreak();
        }
    }

    // Ремонт инструмента
    void repair(int amount) {
        durability += amount;
        if (durability > maxDurability) {
            durability = maxDurability;
        }
        cout << "Repairing the " << name << ". Durability now: " << durability << "/" << maxDurability << endl;
    }

    // Виртуальная функция, вызываемая при поломке
    virtual void onBreak() {
        cout << "The " << name << " breaks with a loud crack!" << endl;
    }

    // Звук инструмента
    virtual void sound() {
        cout << "I am a tool, hear me clang!" << endl;
    }

    // Зачарование (улучшение)
    void enchant(int dmgBonus, int speedBonus) {
        damage += dmgBonus;
        miningSpeed += speedBonus;
        cout << "The " << name << " is enchanted! Damage: " << damage << ", Mining speed: " << miningSpeed << endl;
    }

    // Геттеры
    int getDurability() const { return durability; }
    int getMaxDurability() const { return maxDurability; }
    string getMaterial() const { return material; }
    string getName() const { return name; }
    int getDamage() const { return damage; }
    int getMiningSpeed() const { return miningSpeed; }

    // Сеттеры
    void setDurability(int d) { durability = d; }
    void setMaterial(const string& m) { material = m; }
    // ... остальные при необходимости
};

// Класс кирки
class Pickaxe : public Tool {
public:
    Pickaxe() : Tool() {}

    Pickaxe(int durability_, int maxDurability_, string material_, string name_, int damage_, int miningSpeed_)
        : Tool(durability_, maxDurability_, material_, name_, damage_, miningSpeed_) {}

    void use()  {
        if (durability <= 0) {
            cout << "The " << name << " pickaxe is broken!" << endl;
            return;
        }
        durability--;
        cout << "Mining stone with " << name << " pickaxe. Durability: " << durability << "/" << maxDurability << endl;
        if (durability <= 0) {
            onBreak();
        }
    }

    void sound()  {
        cout << "Tink! Tink! Tink!" << endl;
    }

    void onBreak()  {
        cout << "The pickaxe shatters into pieces!" << endl;
    }
};

// Класс топора
class Axe : public Tool {
public:
    Axe() : Tool() {}

    Axe(int durability_, int maxDurability_, string material_, string name_, int damage_, int miningSpeed_)
        : Tool(durability_, maxDurability_, material_, name_, damage_, miningSpeed_) {}

    void use()  {
        if (durability <= 0) {
            cout << "The " << name << " axe is broken!" << endl;
            return;
        }
        durability--;
        cout << "Chopping wood with " << name << " axe. Durability: " << durability << "/" << maxDurability << endl;
        if (durability <= 0) {
            onBreak();
        }
    }

    void sound()  {
        cout << "Thwack! Thwack! Thwack!" << endl;
    }

    void onBreak()  {
        cout << "The axe handle snaps!" << endl;
    }
};

// Класс лопаты
class Shovel : public Tool {
public:
    Shovel() : Tool() {}

    Shovel(int durability_, int maxDurability_, string material_, string name_, int damage_, int miningSpeed_)
        : Tool(durability_, maxDurability_, material_, name_, damage_, miningSpeed_) {}

    void use()  {
        if (durability <= 0) {
            cout << "The " << name << " shovel is broken!" << endl;
            return;
        }
        durability--;
        cout << "Digging dirt with " << name << " shovel. Durability: " << durability << "/" << maxDurability << endl;
        if (durability <= 0) {
            onBreak();
        }
    }

    void sound()  {
        cout << "Schff! Schff! Schff!" << endl;
    }

    void onBreak()  {
        cout << "The shovel blade cracks!" << endl;
    }
};

// Класс меча
class Sword : public Tool {
public:
    Sword() : Tool() {}

    Sword(int durability_, int maxDurability_, string material_, string name_, int damage_, int miningSpeed_)
        : Tool(durability_, maxDurability_, material_, name_, damage_, miningSpeed_) {}

    void use()  {
        if (durability <= 0) {
            cout << "The " << name << " sword is broken!" << endl;
            return;
        }
        durability--;
        cout << "Attacking with " << name << " sword, dealing " << damage << " damage. Durability: " << durability << "/" << maxDurability << endl;
        if (durability <= 0) {
            onBreak();
        }
    }

    void sound()  {
        cout << "Whoosh! Slash!" << endl;
    }

    void onBreak()  {
        cout << "The sword blade shatters!" << endl;
    }
};

// Класс мотыги
class Hoe : public Tool {
public:
    Hoe() : Tool() {}

    Hoe(int durability_, int maxDurability_, string material_, string name_, int damage_, int miningSpeed_)
        : Tool(durability_, maxDurability_, material_, name_, damage_, miningSpeed_) {}

    void use()  {
        if (durability <= 0) {
            cout << "The " << name << " hoe is broken!" << endl;
            return;
        }
        durability--;
        cout << "Tilling soil with " << name << " hoe. Durability: " << durability << "/" << maxDurability << endl;
        if (durability <= 0) {
            onBreak();
        }
    }

    void sound()  {
        cout << "Scrape! Scrape! Scrape!" << endl;
    }

    void onBreak()  {
        cout << "The hoe bends and breaks!" << endl;
    }
};

int main() {
    // Создаём инструменты
    Pickaxe diamondPick(1561, 1561, "diamond", "Diamond Pickaxe", 5, 8);
    Axe ironAxe(250, 250, "iron", "Iron Axe", 7, 6);
    Shovel stoneShovel(131, 131, "stone", "Stone Shovel", 2, 4);
    Sword woodenSword(59, 59, "wood", "Wooden Sword", 4, 2);
    Hoe goldHoe(32, 32, "gold", "Golden Hoe", 1, 12);

    cout << "\n--- Testing tools ---\n" << endl;

    // Используем инструменты
    diamondPick.use();
    diamondPick.sound();

    ironAxe.use();
    ironAxe.sound();

    stoneShovel.use();
    stoneShovel.sound();

    woodenSword.use();
    woodenSword.sound();

    goldHoe.use();
    goldHoe.sound();

    cout << "\n--- Repair and enchant ---\n" << endl;

    // Ремонт и зачарование
    ironAxe.repair(50);
    diamondPick.enchant(2, 3);

    cout << "\n--- Breaking a tool ---\n" << endl;

    // Доведём до поломки деревянный меч
    for (int i = 0; i < 60; ++i) {
        woodenSword.use();
    }

    cout << "\n--- Final stats ---\n" << endl;
    cout << diamondPick.getName() << " durability: " << diamondPick.getDurability() << "/" << diamondPick.getMaxDurability() << endl;
    cout << ironAxe.getName() << " durability: " << ironAxe.getDurability() << "/" << ironAxe.getMaxDurability() << endl;
    cout << stoneShovel.getName() << " durability: " << stoneShovel.getDurability() << "/" << stoneShovel.getMaxDurability() << endl;
    cout << woodenSword.getName() << " durability: " << woodenSword.getDurability() << "/" << woodenSword.getMaxDurability() << endl;
    cout << goldHoe.getName() << " durability: " << goldHoe.getDurability() << "/" << goldHoe.getMaxDurability() << endl;

    return 0;
}