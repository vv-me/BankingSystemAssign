CREATE TABLE Account_Manager(
	ManId INT auto_increment NOT NULL,
    CustomerId int,
    ManagerId int,
    AssignedDate datetime DEFAULT CURRENT_TIMESTAMP(),
	PRIMARY KEY(ManId),
	FOREIGN KEY (CustomerId)
	REFERENCES customer(CustomerId),
	FOREIGN KEY (ManagerId)
	REFERENCES employee(EmployeeId) ON DELETE RESTRICT
	);