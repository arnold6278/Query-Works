create database knowledge_mining
go


CREATE DATABASE Candidate;

USE Candidate;

CREATE TABLE cadets(
    id_no INT PRIMARY KEY,
    name VARCHAR(50),
    surname VARCHAR(50),
    age INT,
    gender VARCHAR(10),
    contact_number VARCHAR(15),
    marital_status VARCHAR(20),
    salary_range VARCHAR(20)
);

INSERT INTO cadets (id_no, name, surname, age, gender, contact_number, marital_status, salary_range) VALUES
(1, 'John', 'Doe', 30, 'Male', '1234567890', 'Single', '30000-40000'),
(2, 'Jane', 'Smith', 28, 'Female', '0987654321', 'Married', '40000-50000'),
(3, 'Alice', 'Johnson', 35, 'Female', '2345678901', 'Single', '50000-60000'),
(4, 'Bob', 'Brown', 40, 'Male', '3456789012', 'Divorced', '60000-70000'),
(5, 'Charlie', 'Davis', 25, 'Male', '4567890123', 'Single', '20000-30000'),
(6, 'Diana', 'Miller', 32, 'Female', '5678901234', 'Married', '45000-55000'),
(7, 'Ethan', 'Wilson', 29, 'Male', '6789012345', 'Single', '35000-45000'),
(8, 'Fiona', 'Moore', 27, 'Female', '7890123456', 'Married', '40000-50000'),
(9, 'George', 'Taylor', 38, 'Male', '8901234567', 'Single', '60000-70000'),
(10, 'Hannah', 'Anderson', 31, 'Female', '9012345678', 'Divorced', '55000-65000'),
(11, 'Ian', 'Thomas', 45, 'Male', '0123456789', 'Married', '70000-80000'),
(12, 'Julia', 'Jackson', 22, 'Female', '1234567890', 'Single', '25000-35000'),
(13, 'Kevin', 'White', 33, 'Male', '2345678901', 'Married', '50000-60000'),
(14, 'Laura', 'Harris', 36, 'Female', '3456789012', 'Single', '60000-70000'),
(15, 'Mike', 'Martin', 41, 'Male', '4567890123', 'Divorced', '65000-75000'),
(16, 'Nina', 'Thompson', 26, 'Female', '5678901234', 'Married', '40000-50000'),
(17, 'Oscar', 'Garcia', 30, 'Male', '6789012345', 'Single', '30000-40000'),
(18, 'Paula', 'Martinez', 34, 'Female', '7890123456', 'Married', '50000-60000'),
(19, 'Quinn', 'Robinson', 39, 'Male', '8901234567', 'Single', '70000-80000'),
(20, 'Rita', 'Clark', 42, 'Female', '9012345678', 'Divorced', '60000-70000')

INSERT INTO cadets(id_no, name, surname, age, gender, contact_number, marital_status, salary_range) VALUES
(21, 'John', 'Doe', 28, 'Male', '0112345678', 'Single', '6000-10000'),
(22, 'Sarah', 'Connor', 24, 'Female', '0123456789', 'Married', '8000-12000'),
(23, 'Michael', 'Smith', 30, 'Male', '0134567890', 'Single', '10000-15000'),
(24, 'Emily', 'Johnson', 26, 'Female', '0145678901', 'Married', '7000-11000'),
(25, 'David', 'Brown', 32, 'Male', '0156789012', 'Divorced', '12000-18000'),
(26, 'Jessica', 'Jones', 29, 'Female', '0167890123', 'Single', '9000-13000'),
(27, 'Daniel', 'Garcia', 35, 'Male', '0178901234', 'Married', '15000-20000'),
(28, 'Laura', 'Martinez', 31, 'Female', '0189012345', 'Single', '8000-14000'),
(29, 'James', 'Hernandez', 27, 'Male', '0190123456', 'Married', '6000-10000'),
(30, 'Sophia', 'Lopez', 25, 'Female', '0201234567', 'Single', '7000-11000')


select * from cadets