#include"BankCount.h"

BankAccount::BankAccount(const std::string& owner, int initial_balance) : m_nbalance(initial_balance),m_sowner(owner){

}

bool BankAccount::deposit(int amount){
    if (amount <= 0)
    {
        return false;
    }else{
        m_nbalance += amount;
        return true;
    }
}

bool BankAccount::withdraw(int amount){
    if (amount <= 0 || amount > m_nbalance)
    {
        return false;
    }else{
        m_nbalance -= amount;
        return true;
    }
}

int BankAccount::balance() const{
    return m_nbalance;
}

const std::string& BankAccount::owner() const{
    return m_sowner;
}