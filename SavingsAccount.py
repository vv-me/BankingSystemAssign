from BankAccount import BankAccount
class SavingsAccount(BankAccount):
    '''CheckingAccount inherits from the BankAccount class. The main additions here will be a 
    higher withdrawal fee than the Checking Account. There is also an interest method.'''
    WITHDRAW_FEE = 2
    def __init__(self, cust_email, interest_rate, account_type , initial_balance = BankAccount.MIN_BALANCE):
        BankAccount.__init__(self, cust_email, account_type, initial_balance)
        self.interest_rate = interest_rate
        
    def compute_interest(self, period):
        return self.balance * ((1 + self.interest_rate ) ** period - 1)   

    def withdraw(self, amount):
        return BankAccount.withdraw(self, amount + SavingsAccount.WITHDRAW_FEE)    
