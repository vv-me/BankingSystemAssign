# Banking System
#### Simulate a banking account system which allows for new customer registration, account creation and closure, deposits, withdrawals, view balance and assignment of account managers. 
#### Main menu provides these options and any errors at any of the stages return control to the Main screen. 

## UML Diagram

[UML](https://github.com/vv-me/BankingSystemAssign/blob/master/UML.jpg)

## Installation and settup
### Clone the repository
```
$ git clone https://github.com/vv-me/BankingSystemAssign.git
```

### Install pymysql
#### To install this package with conda run:
```
conda install -c anaconda pymysql
```
### Install MySql

[MySql](https://dev.mysql.com/downloads/installer/)

### Database set up and creation
_Create MySQL database called SpringBoardBankingSystem(The script has username as root, password as croak and server name as localhost - Not parameterised yet)_

#### Run the following DMLs in the same order 

1. Customer_MySQL.sql DDL script
2. Employee_MySQL.sql DDL script
3. Employee_INSERT.sql DML script
4. Account_Manager_MySQL.sql DDL script
5. Account_MySQL.sql DDL script

