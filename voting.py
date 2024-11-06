from flask import Flask, render_template, request
from web3 import Web3

class BankAccount:
    def __init__(self):
        self.balance = 0
        self.last_depositor = None
        self.depositors = []

    def deposit(self, amount, depositor):
        if amount <= 0:
            return "Amount must be positive."
        self.balance += amount
        self.last_depositor = depositor
        self.depositors.append(depositor)
        return f"Deposited {amount} by {depositor}."

    def withdraw(self, amount):
        if amount <= 0:
            return "Amount must be positive."
        elif amount > self.balance:
            return "Insufficient balance."
        self.balance -= amount
        return f"Amount withdrawn: {amount}. Remaining balance: {self.balance}"

    def get_balance(self):
        return f"The balance is {self.balance}"

    def get_last_depositor(self):
        return f"The last depositor is {self.last_depositor}"

    def get_all_depositors(self):
        return f"All depositors: {', '.join(self.depositors)}"

app = Flask(__name__)
account = BankAccount()

@app.route('/voting', methods=['GET', 'POST'])
def home():
    message = ""
    if request.method == 'POST':
        if 'deposit' in request.form:
            amount = int(request.form['deposit_amount'])
            depositor = request.form['depositor_name']
            message = account.deposit(amount, depositor)
        elif 'withdraw' in request.form:
            amount = int(request.form['withdraw_amount'])
            message = account.withdraw(amount)
    
    balance = account.get_balance()
    all_depositors = account.get_all_depositors()
    last_depositor = account.get_last_depositor()
    return render_template('index.html', balance=balance, all_depositors=all_depositors,
                           last_depositor=last_depositor, message=message)

if __name__ == "__main__":
    app.run(debug=True)
