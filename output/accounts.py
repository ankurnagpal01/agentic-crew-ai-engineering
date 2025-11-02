class Account:
    def __init__(self, username: str, initial_deposit: float):
        """
        Initialize a new account with a username and an initial deposit.
        
        :param username: The name of the user for the account
        :param initial_deposit: The initial amount of money to deposit
        """
        self.username = username
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []
        self.initial_deposit = initial_deposit

    def deposit(self, amount: float) -> None:
        """
        Deposit a specified amount into the account.
        
        :param amount: Amount to deposit
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        
        self.balance += amount
        self.transactions.append(f"Deposited ${amount:.2f}")

    def withdraw(self, amount: float) -> None:
        """
        Withdraw a specified amount from the account.
        
        :param amount: Amount to withdraw
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance - amount < 0:
            raise ValueError("Insufficient funds for withdrawal.")
        
        self.balance -= amount
        self.transactions.append(f"Withdrew ${amount:.2f}")

    def buy_shares(self, symbol: str, quantity: int) -> None:
        """
        Buy a specified quantity of shares of a given symbol.
        
        :param symbol: The stock symbol to buy
        :param quantity: Number of shares to buy
        """
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
        """
        Sell a specified quantity of shares of a given symbol.
        
        :param symbol: The stock symbol to sell
        :param quantity: Number of shares to sell
        """
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
        """
        Calculate the total value of the user's portfolio.
        
        :return: Total portfolio value
        """
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def calculate_profit_loss(self) -> float:
        """
        Calculate the profit or loss from the initial deposit.
        
        :return: Profit or loss
        """
        return self.calculate_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        """
        Get the current holdings of the user.
        
        :return: A dictionary of holdings and their quantities
        """
        return self.holdings

    def get_profit_loss(self) -> float:
        """
        Get the current profit or loss of the user.
        
        :return: Current profit or loss
        """
        return self.calculate_profit_loss()

    def list_transactions(self) -> list:
        """
        List all transactions made by the user.
        
        :return: A list of transactions
        """
        return self.transactions


def get_share_price(symbol: str) -> float:
    """
    A mock function to get the share price for a given symbol.
    :param symbol: Stock symbol to fetch price for.
    :return: Current price of the share.
    """
    prices = {
        'AAPL': 150.00,
        'TSLA': 700.00,
        'GOOGL': 2800.00
    }
    return prices.get(symbol, 0.0)