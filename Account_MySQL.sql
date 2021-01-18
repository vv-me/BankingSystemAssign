CREATE TABLE bankaccount(
	AccountId INT auto_increment NOT NULL,
	CustomerEmailId NVARCHAR(500) NOT NULL,
    CustId int,
	Balance FLOAT NULL,
    AccountType NVARCHAR(500) NULL,
    InterestLastCalculated date,
    CreatedDate datetime DEFAULT CURRENT_TIMESTAMP(),
	PRIMARY KEY (AccountId));
