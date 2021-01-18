from datetime import datetime, date
from sqlalchemy import create_engine, Table, MetaData, select, func, alias 

class AccountManager:
    def assign_manager(self, customer_email):
        '''
        Manager is assigned randomly for a customer. One manager per customer. Database entry is made
        in the account_manager MySQL table.
        '''
        engine = create_engine('mysql+pymysql://root:croak@localhost/SpringBoardBankingSystem')
        connection = engine.connect()
        metadata = MetaData()
        customer = Table('customer', metadata, autoload=True,autoload_with=engine)
        cust_id_res = connection.execute(select([customer.c.CustomerId]).where(customer.c.Email == customer_email)).fetchall()
        cust_id = cust_id_res[0].CustomerId
        acc_manager = Table('Account_Manager', metadata, autoload=True,autoload_with=engine)
        acc_man_res = connection.execute(select([func.count().label('CountExistingEntries')]).where(acc_manager.c.CustomerId == cust_id)).fetchall()
        if(acc_man_res[0].CountExistingEntries == 0):
            employee = Table('employee', metadata, autoload=True,autoload_with=engine)    
            emp_res = connection.execute(select([employee.c.EmployeeId.label('emp_id')]).select_from(employee).order_by(func.rand()).limit(1)).fetchmany(size = 1)
            ins = (acc_manager.insert().values(CustomerId = cust_id, ManagerId = emp_res[0].emp_id)
            )
            connection.execute(ins)
            #TBD return assigned account manager name and email to user. 
            print('\nAccount manager assigned successfully.\n\nRETURNING TO MAIN MENU.')   
        else:
            raise ValueError('Account managesr already assigned for this customer.\n\nRETURNING TO MAIN MENU.')           

        #TBD Need to implement account manager assignment based on number of accounts per manager - If first entry
        #then pick the most experienced employee. If not then pick based on fewest assigned accounts.
        #Current implementation is random records
        '''
        results = connection.execute(select([func.count().label('CountExistingEntries')]).select_from(acc_manager)).fetchall()
        if(results[0].CountExistingEntries == 0):
            employee = Table('employee', metadata, autoload=True,autoload_with=engine)
            emp_res = connection.execute(select([employee.c.EmployeeId.label('A')]).select_from(employee).order_by(employee.c.DOJ.desc())).fetchmany(size = 1)
            print(emp_res[0].A)'''

        