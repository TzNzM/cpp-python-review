#include<string>

class BankAccount {
private:
    std::string m_sowner;
    int m_nbalance;

public:
    BankAccount(const std::string& owner, int initial_balance);

    bool deposit(int amount);
    bool withdraw(int amount);

    int balance() const;
    const std::string& owner() const;
};