USE PERSONDATABASE

/*********************
Hello! 

Please use the test data provided in the file 'PersonDatabase' to answer the following
questions. Please also import the dbo.Contacts flat file to a table for use. 

All answers should be executable on a MS SQL Server 2012 instance. 

***********************



QUESTION 1

The table dbo.Risk contains calculated risk scores for the population in dbo.Person. Write a 
query or group of queries that return the patient name, and their most recent risk level(s). 
Any patients that dont have a risk level should also be included in the results. 

**********************/
SELECT Person.PersonName, Risk.RiskLevel, Risk.RiskDateTime
FROM dbo.Person
Left Join dbo.Risk ON Person.PersonID = Risk.PersonID
ORDER BY PersonName, Risk.RiskDateTime DESC
/**********************

QUESTION 2


The table dbo.Person contains basic demographic information. The source system users 
input nicknames as strings inside parenthesis. Write a query or group of queries to 
return the full name and nickname of each person. The nickname should contain only letters 
or be blank if no nickname exists.

**********************/

SELECT PersonName, SUBSTRING(PersonName, PATINDEX('%[(]%', PersonName) + 1, (PATINDEX('%[)]%', PersonName) - PATINDEX('%[(]%', PersonName) - 1)) AS Nickname FROM dbo.Person
WHERE PATINDEX('%[)]%', PersonName) - PATINDEX('%[(]%', PersonName) != 0;

/**********************

QUESTION 6

Write a query to return risk data for all patients, all payers 
and a moving average of risk for that patient and payer in dbo.Risk. 

**********************/
SELECT RiskScore, Person.PersonID, PersonName, AttributedPayer
FROM dbo.Person
Inner Join dbo.Risk ON Person.PersonID = Risk.PersonID
SELECT DISTINCT Risk.PersonID, AttributedPayer, AVG(Risk.RiskScore) 
OVER (PARTITION BY Risk.PersonID, AttributedPayer) AS MovingAverage
FROM dbo.Risk
Inner Join dbo.Person ON Person.PersonID = Risk.PersonID