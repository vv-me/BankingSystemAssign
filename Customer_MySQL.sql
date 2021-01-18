USE SpringBoardBankingSystem;
CREATE TABLE Customer (
    CustomerId INT auto_increment NOT NULL,
    FirstName NVARCHAR(500) NOT NULL,
    LastName NVARCHAR(500) NOT NULL,
    DOB DATE NOT NULL,
    AddressLine1 NVARCHAR(500) NOT NULL,
    AddressLine2 NVARCHAR(500) NULL,
    City NVARCHAR(500) NOT NULL,
    State NVARCHAR(500) NOT NULL,
    Zipcode NVARCHAR(500) NOT NULL,
    Country NVARCHAR(500) NOT NULL,
    Email NVARCHAR(500) NOT NULL,
	Phone NVARCHAR(500) NOT NULL,
    SSN NVARCHAR(500) NOT NULL,
    CustomerCreationDate datetime DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (CustomerId));



