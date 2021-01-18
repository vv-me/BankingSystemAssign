from customer import Customer
from BankAccount import BankAccount
from CheckingAccount import CheckingAccount
from SavingsAccount import SavingsAccount
from account_manager import AccountManager
from datetime import datetime, date
from sqlalchemy import create_engine, Table, MetaData, select, func, alias 
import re 
'''
Driver program. Displays main menu. Customer needs to first be registered. Account manager can be assigned 
if necessary. One account manager is assigned per customer(randomly chosen). Multiple customers can 
be assigned to the same manager. 
Multiple accounts can be created for the same customer. Existing accounts can be accessed for withdrawal,
deposit and checking balance.
'''
while True:
    print('\n')
    print('WELCOME TO SPRINGBOARD BANKING SYSTEM!\n')
    print('MAIN MENU :\n')
    print('1. Customer Registration(enter 1)')
    print('2. Assign Account Manager(enter 2)')
    print('3. Account Creation/Access(enter 3)')
    print('4. Exit(enter 4)')
    option = input('\nPlease input the number associated with the option : ') 
    if(option == '1'):
        try:
            '''Customer details entry with data checks'''
            first_name = input('Enter first name(Letters or spaces only): ')
            if not all(c.isalpha() or c.isspace() for c in first_name):
                raise ValueError("Invalid character. Only letters and spaces are allowed in the first name.")
            last_name = input('Enter last name(Letter, spaces or numbers only): ')
            if not all(c.isalpha() or c.isspace() or c.isdigit()  for c in last_name):
                raise ValueError("Invalid character. Only letters, spaces and numbers are allowed in the last name.")   
            dob = input('Enter date of birth in the format YYYY-MM-DD: ')
            if dob != datetime.strptime(dob, '%Y-%m-%d').strftime('%Y-%m-%d'):
                raise ValueError("Incorrect format of date. Enter dob as YYYY-MM-DD")
            if Customer.calculate_age(dob) < 18:
                raise ValueError("Underage candidate. Minimum age to create account is 18 years")
            address_line1 = input('Enter Address line 1: ')
            address_line2 = input('Enter Address line 2: ')
            city = input('Enter City: ')
            state = input('Enter State: ')
            zipcode = input('Enter Zipcode: ')
            country = input('Enter Country: ')
            email = input('Enter email: ')
            if not (re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',email)):  
                raise ValueError("Invalid email.")
            phone = input('Enter Phone Number in the format XXX-XXX-XXXX: ')
            if not (re.search('\d{3}-\d{3}-\d{4}',phone)):  
                raise ValueError("Phone format is incorrect. Please enter in this format - XXX-XXX-XXXX") 
            ssn = input('Enter SSN in the format XXX-XX-XXXX: ')
            if not (re.search('\d{3}-\d{2}-\d{4}',ssn)):  
                raise ValueError("SSN format is incorrect. Please enter in this format - XXX-XX-XXXX")
            cust = Customer( first_name, last_name, dob, address_line1, address_line2, city, state, zipcode, country, email, phone, ssn)
            cust.register_customer()
            #cust.first_name = '$$$$$'
        except ValueError as inst:
            print(inst.args[0]+'\n\nRETURNING TO MAIN MENU.')
            
            
    elif(option == '2'):
        '''Assignment of account manager for an existing customer. Managers are assigned at the customer
        level and not the account level'''
        email_id = input('Enter existing customer email: ')
        engine = create_engine('mysql+pymysql://root:croak@localhost/SpringBoardBankingSystem')
        connection = engine.connect()
        metadata = MetaData()
        customer = Table('Customer', metadata, autoload=True,autoload_with=engine)
        results = connection.execute(select([func.count().label('CountExistingEmail')]).where(customer.c.Email == email_id)).fetchall()
        if(results[0].CountExistingEmail == 0):
            print('Email id does not exist. Please enter registered email id or register the customer. \n\nRETURNING TO MAIN MENU.')
            continue
        else:
            try:
                acc_m = AccountManager()
                acc_m.assign_manager(email_id)
            except ValueError as inst:
                print(inst.args[0])
    
    elif(option == '3'):
        '''Bank account create/access/delete. Customer needs to be registered for any of these
        actions. Registered email needs to be available. Please note the account number on creation
        for future access.'''
        flg = 0
        email_id = input('Enter existing customer email: ')
        engine = create_engine('mysql+pymysql://root:croak@localhost/SpringBoardBankingSystem')
        connection = engine.connect()
        metadata = MetaData()
        customer = Table('Customer', metadata, autoload=True,autoload_with=engine)
        results = connection.execute(select([func.count().label('CountExistingEmail')]).where(customer.c.Email == email_id)).fetchall()
        if(results[0].CountExistingEmail == 0):
            print('Email id does not exist. Please enter registered email id or register the customer. Returning to Main Menu.')
            continue
        else:
            opt = int(input('\nWhat would you like to do?\n\n1. Create new account : \n2. Access existing account(for deposits, withdrawals, balance check) : \n3. Delete an existing account : \n\nEnter option 1, 2 or 3: '))
            if (opt == 1):
                deposit = float(input('Enter initial deposit amount in dollars(Minumum amount is $' + str(BankAccount.MIN_BALANCE) + ') : '))
                while True:
                    if deposit < BankAccount.MIN_BALANCE:
                        print('Initial deposit lesser than the minimum amount required to start an account. Please deposit atleast $'+ str(BankAccount.MIN_BALANCE)+'.')
                        cont = int(input('Would you like to re-enter the deposit amount(option 1) or return to main menu(option 2)[1/2] : '))
                        if (cont == 1):
                            deposit = float(input('Enter initial deposit amount in dollars(Minumum amount is $100): '))
                            continue
                        else:
                            flg = 1
                            break
                    else:
                        break    
                if (flg == 1):
                    continue
                
                cs = input('Do you want to open a checking[C] or savings[S] account? [C/S] : ').upper()
                if(cs == 'C'):
                    ba = CheckingAccount(email_id, cs, deposit )
                elif(cs == 'S'):
                    interest_rate = 0.015
                    ba = SavingsAccount(email_id, interest_rate, cs, deposit)
                else:
                    print('Incorrect entry.\nRETURNING TO MAIN MENU.')   
                    continue
                cont = input('Do you want to deposit more into your current account?[Y/N] : ').upper()
                if (cont == 'Y'):
                    dep = float(input('Enter the deposit amount in dollars: '))
                    ba.deposit(dep)
                cont = input('Do you want to withdraw money from your current account?[Y/N] : ').upper()
                if (cont == 'Y'):
                    withdraw = float(input('Enter withdrawal amount in dollars(Minumum balance is $' + str(BankAccount.MIN_BALANCE) + ') :'))
                    try:
                        ba.withdraw(withdraw)
                    except ValueError as inst:
                        print(inst.args[0])  
                cont = input('Do you want to see your current balance?[Y/N] : ')
                if (cont == 'Y'):
                    print('Current balance is $ '+ str(ba.balance) + '.')
            elif (opt == 2):
                bank_acc = Table('bankaccount', metadata, autoload=True,autoload_with=engine)
                acc_ids = connection.execute(select([bank_acc.c.AccountId, bank_acc.c.Balance]).where(bank_acc.c.CustomerEmailId == email_id)).fetchall()
                if(len(acc_ids) == 0):
                    print('This customer has no associated bank accounts. Please create a bank account. \n\nRETURNING TO MAIN MENU.')
                    continue
                print('\nThis is your list of accounts.\n')
                acc = []
                for x in acc_ids:
                    print(x[0])
                    acc.append(x[0])
                acc_no = int(input('\nEnter the account number you want to access : '))
                try:
                    if acc_no not in acc:
                        raise ValueError('Incorrect Account number.')
                except ValueError as inst:
                        print(inst.args[0]+'\n\nRETURNING TO MAIN MENU.')
                        continue

                for x in acc_ids:
                    if (x[0] == acc_no):
                        bal = x[1]
                cont = input('Do you want to deposit money into your current account?[Y/N] : ').upper()
                if (cont == 'Y'):
                    dep = float(input('Enter the deposit amount in dollars: '))
                    bank_acc = Table('bankaccount', metadata, autoload=True,autoload_with=engine)
                    stmt = bank_acc.update().\
                    where(bank_acc.c.AccountId==acc_no).\
                    values(Balance=bal+dep)
                    connection.execute(stmt)    

                cont = input('Do you want to withdraw money from your current account?[Y/N] : ').upper()
                if (cont == 'Y'):
                    acc_ids = connection.execute(select([bank_acc.c.AccountId, bank_acc.c.Balance, bank_acc.c.AccountType]).where(bank_acc.c.CustomerEmailId == email_id)).fetchall()
                    for x in acc_ids:
                        if (x[0] == acc_no):
                            acc_type = x[2]
                            bal = x[1]
                            break
                    withdraw = float(input('Enter withdrawal amount in dollars(Minumum balance is $' + str(BankAccount.MIN_BALANCE) + ') : '))
                    if(acc_type == 'C'):
                        new_bal = bal - (withdraw + CheckingAccount.WITHDRAW_FEE)
                        if(new_bal >= BankAccount.MIN_BALANCE):
                            balance = new_bal
                        else:
                            print('Withdrawal amount will lower the available balance below the minimum. Please enter a lower amount.')
                            print('\nRETURNING TO MAIN MENU.')
                            continue
                    elif(acc_type == 'S'):
                        new_bal = bal - (withdraw + SavingsAccount.WITHDRAW_FEE)  
                        if(new_bal >= BankAccount.MIN_BALANCE):
                            balance = new_bal
                        else:
                            print('Withdrawal amount will lower the available balance below the minimum. Please enter a lower amount.')
                            print('\nRETURNING TO MAIN MENU.')
                            continue
                    

                    bank_acc = Table('bankaccount', metadata, autoload=True,autoload_with=engine)
                    stmt = bank_acc.update().\
                    where(bank_acc.c.AccountId==acc_no).\
                    values(Balance=balance)
                    connection.execute(stmt)       
                    
                    
                cont = input('Do you want to see your current balance?[Y/N] : ').upper()
                if (cont == 'Y'):
                    acc_ids = connection.execute(select([bank_acc.c.AccountId, bank_acc.c.Balance]).where(bank_acc.c.CustomerEmailId == email_id)).fetchall()
                    for x in acc_ids:
                        if (x[0] == acc_no):
                            bal = x[1]
                            break
                    print('Current balance is $ '+ str(bal) + '.') 
            elif (opt == 3):
                bank_acc = Table('bankaccount', metadata, autoload=True,autoload_with=engine)
                acc_ids = connection.execute(select([bank_acc.c.AccountId]).where(bank_acc.c.CustomerEmailId == email_id)).fetchall()
                print('This is your list of accounts.\n')
                acc = []
                for x in acc_ids:
                    print(x[0])
                    acc.append(x[0])    
                acc_no = int(input('\nPlease pick the account number of the account you want to delete : '))
                if acc_no not in acc:
                    raise ValueError('Incorrect Account number.\n\nRETURNING TO MAIN MENU.')
                print('Deleting..')
                bank_acc = Table('bankaccount', metadata, autoload=True,autoload_with=engine)
                connection.execute(bank_acc.delete().where(bank_acc.c.AccountId == acc_no))
                print('Deleted!')

            else:
                print('Incorrect option entered.\n\nRETURNING TO MAIN MENU.')
                continue
    elif(option == '4'):
        print('Goodbye!')
        break

    else :
        print('Incorrect entry. Please select from options. Returning to Main Menu.')
        continue


         

