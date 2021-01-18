from BankAccount import BankAccount
class CheckingAccount(BankAccount):
    '''CheckingAccount inherits from the BankAccount class. The main additions here will be a withdrawal fee'''
    WITHDRAW_FEE = 1
    def __init__(self, cust_email, account_type, initial_balance = BankAccount.MIN_BALANCE):
        #Call the parent init
        BankAccount.__init__(self, cust_email ,account_type, initial_balance)
        
    def withdraw(self, amount):
        '''Calls the parent BankAccount withdraw method but adds a fee to the withdrawal amount'''
        return BankAccount.withdraw(self, amount + CheckingAccount.WITHDRAW_FEE)


