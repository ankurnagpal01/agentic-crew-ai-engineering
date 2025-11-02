import gradio as gr
from accounts import Account

# Create a single account instance
account = Account("DemoUser", 1000.0)  # Starting with $1000

def create_account(username, initial_deposit):
    global account
    account = Account(username, initial_deposit)
    return "Account created successfully!"

def deposit_funds(amount):
    try:
        account.deposit(amount)
        return f"Deposited: ${amount:.2f}. New balance: ${account.balance:.2f}"
    except ValueError as e:
        return str(e)

def withdraw_funds(amount):
    try:
        account.withdraw(amount)
        return f"Withdrew: ${amount:.2f}. New balance: ${account.balance:.2f}"
    except ValueError as e:
        return str(e)

def buy_shares(symbol, quantity):
    try:
        account.buy_shares(symbol, quantity)
        return f"Bought {quantity} shares of {symbol}. New balance: ${account.balance:.2f}"
    except ValueError as e:
        return str(e)

def sell_shares(symbol, quantity):
    try:
        account.sell_shares(symbol, quantity)
        return f"Sold {quantity} shares of {symbol}. New balance: ${account.balance:.2f}"
    except ValueError as e:
        return str(e)

def portfolio_value():
    value = account.calculate_portfolio_value()
    return f"Total Portfolio Value: ${value:.2f}"

def profit_loss():
    profit_loss_value = account.get_profit_loss()
    return f"Profit/Loss: ${profit_loss_value:.2f}"

def holdings():
    return str(account.get_holdings())

def transactions():
    return "\n".join(account.list_transactions())

with gr.Blocks() as demo:
    gr.Markdown("# Trading Account Management")
    with gr.Row():
        username_input = gr.Textbox(label="Username")
        deposit_input = gr.Number(label="Initial Deposit", default=1000)
        create_button = gr.Button("Create Account")
    
    create_button.click(create_account, inputs=[username_input, deposit_input], outputs="text")
    
    with gr.Row():
        deposit_amount = gr.Number(label="Deposit Amount")
        deposit_button = gr.Button("Deposit")
    
    deposit_button.click(deposit_funds, inputs=deposit_amount, outputs="text")

    with gr.Row():
        withdraw_amount = gr.Number(label="Withdraw Amount")
        withdraw_button = gr.Button("Withdraw")
    
    withdraw_button.click(withdraw_funds, inputs=withdraw_amount, outputs="text")

    with gr.Row():
        buy_symbol = gr.Textbox(label="Buy Symbol (AAPL, TSLA, GOOGL)")
        buy_quantity = gr.Number(label="Quantity to Buy")
        buy_button = gr.Button("Buy Shares")
    
    buy_button.click(buy_shares, inputs=[buy_symbol, buy_quantity], outputs="text")

    with gr.Row():
        sell_symbol = gr.Textbox(label="Sell Symbol (AAPL, TSLA, GOOGL)")
        sell_quantity = gr.Number(label="Quantity to Sell")
        sell_button = gr.Button("Sell Shares")
    
    sell_button.click(sell_shares, inputs=[sell_symbol, sell_quantity], outputs="text")

    with gr.Row():
        portfolio_button = gr.Button("Check Portfolio Value")
    
    portfolio_button.click(portfolio_value, outputs="text")

    with gr.Row():
        profit_loss_button = gr.Button("Check Profit/Loss")
    
    profit_loss_button.click(profit_loss, outputs="text")

    with gr.Row():
        holdings_button = gr.Button("View Holdings")
    
    holdings_button.click(holdings, outputs="text")

    with gr.Row():
        transactions_button = gr.Button("View Transactions")
    
    transactions_button.click(transactions, outputs="text")

demo.launch()