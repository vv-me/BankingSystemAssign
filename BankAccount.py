from sqlalchemy import create_engine, Table, MetaData, select, func, alias, update
from customer import Customer

class BankAccount:
    '''BankAccount is the parent class. A bank account can be created for a registered customer.
    Customers are identified using their email ids'''
    MIN_BALANCE = 100
    def get_cust_id(self, connection, customer, metadata):
        '''Method to retrieve the CustomerId from the database related to the customer email entered.'''
        cust_id_res = connection.execute(select([customer.c.CustomerId]).where(customer.c.Email == self.cust_email)).fetchall()
        return cust_id_res[0].CustomerId

    def make_db_entry(self, connection,bank_acc, metadata):
        '''Method to make an entry into the bankaccount MySQL table. The primary key, AccountId is returned
        to the constructor which is saved in the class variable.'''
        ins = (bank_acc.insert().values(CustomerEmailId = self.cust_email, CustId = self.cust_id
            , Balance = self._balance, AccountType = self.account_type))
        acc_id = connection.execute(ins)
        return acc_id.inserted_primary_key
        
    def __init__(self, cust_email, account_type, initial_balance):
        self.cust_email = cust_email
        self.account_type = account_type
        engine = create_engine('mysql+pymysql://root:croak@localhost/SpringBoardBankingSystem')
        connection = engine.connect()
        metadata = MetaData()
        customer = Table('Customer', metadata, autoload=True,autoload_with=engine)
        self.cust_id = self.get_cust_id(connection,customer,metadata)
        self._balance = initial_balance
        bank_acc = Table('bankaccount', metadata, autoload=True,autoload_with=engine)
        self.acc_number = self.make_db_entry(connection,bank_acc, metadata)[0]
        print('Account successfully created!')
        print('Account number is '+ str(self.acc_number)+'. Please note this for future transactions.')

    @property
    def balance(self):
        return self._balance    
    
    @balance.setter
    def balance(self, amount): 
        self._balance = amount
        engine = create_engine('mysql+pymysql://root:croak@localhost/SpringBoardBankingSystem')
        connection = engine.connect()
        metadata = MetaData()
        bank_acc = Table('bankaccount', metadata, autoload=True,autoload_with=engine)
        stmt = bank_acc.update().\
            where(bank_acc.c.CustId==self.cust_id).\
            values(Balance=amount)
        connection.execute(stmt)
        
    def deposit(self, amount): 
        '''Calls the balance setter method which also makes an update against that record in the database'''
        int_bal = self._balance + amount
        self.balance = int_bal 
        print('Deposit successful!')

    def withdraw(self, amount):
        '''Calls the balance setter method which also makes an update against that record in the database. 
        Withdrawal is allowed only if the balance after withdrawal will be greater than or equal to the
        Minumum balance defined'''
        if (self.balance - amount >= BankAccount.MIN_BALANCE):
            self.balance -= amount 
            print('Withdrawal successful!')  
        else:
            raise ValueError('Minimum balance in account needs to be ' + str(BankAccount.MIN_BALANCE)+ '. Please enter a lower withdrawal amount.')      
       