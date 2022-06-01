USE PERSONDATABASE
Go

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
/*The with clause can be used in a CREATE VIEW statement as part of its defining SELECT statement.*/
with temp (PersonName, RiskLevel, RiskDateTime, rnk) as (
select PersonName, RiskLevel, RiskDateTime, Rank() over (partition by PersonName order by RiskDateTime desc) from dbo.Person
left outer join dbo.Risk on dbo.Risk.PersonID = dbo.Person.PersonID
)
select PersonName, RiskLevel, RiskDateTime from temp where rnk = 1;


/**********************

QUESTION 2


The table dbo.Person contains basic demographic information. The source system users 
input nicknames as strings inside parenthesis. Write a query or group of queries to 
return the full name and nickname of each person. The nickname should contain only letters 
or be blank if no nickname exists.

**********************/



/**********************

QUESTION 6

Write a query to return risk data for all patients, all payers 
and a moving average of risk for that patient and payer in dbo.Risk. 

**********************/




