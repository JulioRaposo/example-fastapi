import pytest
from app.calculations import add, BankAccount, InsufficientFunds


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1,num2,expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    print('test add function')
    sum = add(num1, num2)
    assert sum == expected


def test_bank_set_amount():
    bank_acccount = BankAccount(50)
    assert bank_acccount.balance == 50


def test_default_bank_account(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_withdraw():
    bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55


@pytest.mark.parametrize("deposited,withdrew,expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000)
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
