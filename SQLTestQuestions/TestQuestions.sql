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
/*The WITH clause can be used in a CREATE VIEW statement as part of its defining SELECT statement.
Rank returns the rank of each row within the partition of a result set. The rank of a row is one plus the number of ranks that come before the row in question.*/
with temp (PersonName, RiskLevel, RiskDateTime, rnk) as (
select PersonName, RiskLevel, RiskDateTime, Rank() over (partition by PersonName order by RiskDateTime desc) from dbo.Person
left outer join dbo.Risk on dbo.Risk.PersonID = dbo.Person.PersonID)
select PersonName, RiskLevel, RiskDateTime from temp where rnk = 1;

/*I copied this answer from another user*/

/**********************

QUESTION 2


The table dbo.Person contains basic demographic information. The source system users 
input nicknames as strings inside parenthesis. Write a query or group of queries to 
return the full name and nickname of each person. The nickname should contain only letters 
or be blank if no nickname exists.

**********************/
/*Like determines whether a specific character string matches a specified pattern. escape_character is a character put in front of a wildcard character 
to indicate that the wildcard is interpreted as a regular character and not as a wildcard. 
escape_character is a character expression that has no default and must evaluate to only one character.

The STUFF function inserts a string into another string. 
It deletes a specified length of characters in the first string at the start position and then inserts the second string into the first string at the start position.

CharIndex function searches for one character expression inside a second character expression, returning the starting position of the first expression if found.*/

select ISNULL(stuff((select PersonName where PersonName LIKE ('%(%') ), CHARINDEX('(', PersonName), len(substring(PersonName,CHARINDEX('(', PersonName) + 1,CHARINDEX(')', PersonName) - CHARINDEX('(', PersonName)-.5)) + 2, ''), PersonName) as FullName, 
substring(PersonName,CHARINDEX('(', PersonName) + 1,CHARINDEX(')', PersonName) - CHARINDEX('(', PersonName)-.5) as NickName
from dbo.Person;

/*I copied this answer from another user*/

/**********************

QUESTION 6

Write a query to return risk data for all patients, all payers 
and a moving average of risk for that patient and payer in dbo.Risk. 

**********************/

select AVG(RiskScore) as PersonAvgRisk from dbo.Risk group by dbo.Risk.PersonID 
select AttributedPayer, AVG(RiskScore) as PayerAvgRisk from dbo.Risk group by dbo.Risk.AttributedPayer
select AVG(RiskScore) as AverageRisk from dbo.Risk group by dbo.Risk.AttributedPayer, dbo.Risk.PersonID



