USE SpringBoardBankingSystem;
CREATE TABLE Employee(
	EmployeeId INT auto_increment NOT NULL,
	EmployeeFirstName NVARCHAR(500) NOT NULL,
	EmployeeLastName NVARCHAR(500) NOT NULL,
	DOJ DATE NOT NULL,
	DOB DATE NOT NULL,
	EmailId NVARCHAR(500) NOT NULL,
	Phone NVARCHAR(500) NOT NULL,
	PRIMARY KEY (EmployeeId));

