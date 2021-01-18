from datetime import datetime, date
from sqlalchemy import create_engine, Table, MetaData, select, func, alias 
import re 

class Customer:
    '''
    Customer class has various attributes related to the customer. All attributes go thru data checks based
    on the rules set on the field. Once the data is verified successfully an entry is made in the MySQL
    customer table on the SPRINGBOARDBANKINGSYSTEM database.
    '''
    def __init__(self, first_name, last_name, dob, address_line1, address_line2, city, state, zipcode, country, email, phone, ssn):
        '''
        Set private attributes.
        '''
        self._first_name = first_name
        self._last_name = last_name 
        self._dob = dob
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.country = country
        self._email = email
        self._phone = phone
        self._ssn = ssn

    def is_valid_firstname(self, name):
        return all(c.isalpha() or c.isspace() for c in name)   

    def is_valid_lastname(name):
        return all(c.isalpha() or c.isspace() or c.isdigit()  for c in name)     

    def calculate_age(dob):
        dob_date = datetime.strptime(dob, '%Y-%m-%d')
        today = date.today() 
        return today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))

    @property    
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        if not (Customer.is_valid_firstname(first_name)) :
            raise ValueError("Invalid character. Only letters and spaces are allowed in the first name.")
        self._first_name = first_name

    @property    
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        if not (Customer.is_valid_lastname(last_name)) :
            raise ValueError("Invalid character. Only letters, spaces and numbers are allowed in the last name.")
        self._last_name = last_name

    @property    
    def dob(self):
        return self._dob

    @dob.setter
    def dob(self, dob):
        if dob != datetime.strptime(dob, '%Y-%m-%d').strftime('%Y-%m-%d'):
            raise ValueError("Incorrect format of date. Enter dob as YYYY-MM-DD")
        if Customer.calculate_age(dob) < 18:
            raise ValueError("Underage candidate. Minimum age to create account is 18 years")

    @property    
    def email(self):
        return self._email

    @email.setter
    def email(self, email):  
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not (re.search(regex,email)):  
            raise ValueError("email format is incorrect.")

    @property    
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, phone):  
        regex = '\d{3}-\d{3}-\d{4}'
        if not (re.search(regex,phone)):  
            raise ValueError("Phone format is incorrect.") 

    @property    
    def ssn(self):
        return self._ssn

    @ssn.setter
    def ssn(self, phone):  
        regex = '\d{3}-\d{2}-\d{4}'
        if not (re.search(regex,ssn)):  
            raise ValueError("SSN format is incorrect.")    

    def register_customer(self):
        '''
        email is unique on the backened customer table. If an existing email is entered, the system throws an error
        and returns to main menu. If not it creates an entry in the table customer.
        '''
        #engine = create_engine('mssql+pyodbc://localhost/SpringBoardBankingSystem?trusted_connection=yes&driver=ODBC+Driver+13+for+SQL+Server')
        engine = create_engine('mysql+pymysql://root:croak@localhost/SpringBoardBankingSystem')
        connection = engine.connect()
        metadata = MetaData()
        customer = Table('Customer', metadata, autoload=True,autoload_with=engine)
        results = connection.execute(select([func.count().label('CountExistingEmail')]).where(customer.c.Email == self.email)).fetchall()
        if(results[0].CountExistingEmail == 0):
            ins = (customer.insert().values(FirstName = self.first_name, LastName = self.last_name
            , DOB = self.dob, AddressLine1 = self.address_line1, AddressLine2 = self.address_line2
            , City = self.city, State = self.state, Zipcode = self.zipcode, Country = self.country 
            , Email = self.email, Phone = self.phone, SSN = self.ssn)
            )
            connection.execute(ins)
            print('\nRegistration successful.\nRETURNING TO MAIN MENU.')
        else:
            raise ValueError('This email id is already registered for a customer. Use unique email id for new registration.')    
    

            

              
  





        


        

        
        
        
