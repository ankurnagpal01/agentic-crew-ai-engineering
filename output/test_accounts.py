import unittest

class Account:
    def __init__(self, username: str, initial_deposit: float):
        self.username = username
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []
        self.initial_deposit = initial_deposit

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.transactions.append(f"Deposited ${amount:.2f}")

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance - amount < 0:
            raise ValueError("Insufficient funds for withdrawal.")
        self.balance -= amount
        self.transactions.append(f"Withdrew ${amount:.2f}")

    def buy_shares(self, symbol: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        share_price = get_share_price(symbol)
        total_cost = share_price * quantity
        if total_cost > self.balance:
            raise ValueError("Insufficient funds to buy shares.")
        self.balance -= total_cost
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        self.transactions.append(f"Bought {quantity} shares of {symbol} at ${share_price:.2f}")

    def sell_shares(self, symbol: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            raise ValueError("Not enough shares to sell.")
        share_price = get_share_price(symbol)
        total_gain = share_price * quantity
        self.balance += total_gain
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.transactions.append(f"Sold {quantity} shares of {symbol} at ${share_price:.2f}")

    def calculate_portfolio_value(self) -> float:
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def calculate_profit_loss(self) -> float:
        return self.calculate_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.holdings

    def get_profit_loss(self) -> float:
        return self.calculate_profit_loss()

    def list_transactions(self) -> list:
        return self.transactions


def get_share_price(symbol: str) -> float:
    prices = {
        'AAPL': 150.00,
        'TSLA': 700.00,
        'GOOGL': 2800.00
    }
    return prices.get(symbol, 0.0)


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account('test_user', 1000.0)

    def test_initialization(self):
        self.assertEqual(self.account.username, 'test_user')
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(self.account.transactions, [])

    def test_deposit(self):
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertIn('Deposited $500.00', self.account.transactions)
        with self.assertRaises(ValueError):
            self.account.deposit(-100)

    def test_withdraw(self):
        self.account.withdraw(200.0)
        self.assertEqual(self.account.balance, 800.0)
        self.assertIn('Withdrew $200.00', self.account.transactions)
        with self.assertRaises(ValueError):
            self.account.withdraw(2000)
        with self.assertRaises(ValueError):
            self.account.withdraw(-50)

    def test_buy_shares(self):
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.balance, 700.0)
        self.assertEqual(self.account.holdings['AAPL'], 2)
        self.assertIn('Bought 2 shares of AAPL at $150.00', self.account.transactions)
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', 10)
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', -5)

    def test_sell_shares(self):
        self.account.buy_shares('AAPL', 2)
        self.account.sell_shares('AAPL', 1)
        self.assertEqual(self.account.holdings['AAPL'], 1)
        self.assertEqual(self.account.balance, 850.0)
        self.assertIn('Sold 1 shares of AAPL at $150.00', self.account.transactions)
        with self.assertRaises(ValueError):
            self.account.sell_shares('AAPL', 2)
        with self.assertRaises(ValueError):
            self.account.sell_shares('GOOGL', 1)

    def test_calculate_portfolio_value(self):
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.calculate_portfolio_value(), 700.0 + 300.0)

    def test_calculate_profit_loss(self):
        self.assertEqual(self.account.calculate_profit_loss(), 0.0)
        self.account.deposit(500.0)
        self.assertGreater(self.account.calculate_profit_loss(), 0.0)

    def test_get_holdings(self):
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.get_holdings(), {'AAPL': 2})

    def test_list_transactions(self):
        self.account.deposit(500.0)
        self.account.withdraw(200.0)
        self.assertEqual(len(self.account.list_transactions()), 2)

if __name__ == '__main__':
    unittest.main()