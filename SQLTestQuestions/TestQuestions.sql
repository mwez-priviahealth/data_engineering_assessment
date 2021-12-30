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
with cte (PersonName, RiskLevel, rnk ) as (
select PersonName, RiskLevel, Rank() over (partition by PersonName order by RiskDateTime desc) from Person
left outer join Risk on Risk.PersonID = Person.PersonID
)
select PersonName, RiskLevel from cte where rnk = 1;



/**********************

QUESTION 2


The table dbo.Person contains basic demographic information. The source system users 
input nicknames as strings inside parenthesis. Write a query or group of queries to 
return the full name and nickname of each person. The nickname should contain only letters 
or be blank if no nickname exists.

**********************/
select ISNULL(stuff((select PersonName where PersonName LIKE ('%(%') ), CHARINDEX('(', PersonName), len(substring(PersonName,CHARINDEX('(', PersonName) + 1,CHARINDEX(')', PersonName) - CHARINDEX('(', PersonName)-.5)) + 2, ''), PersonName) as FullName, 
substring(PersonName,CHARINDEX('(', PersonName) + 1,CHARINDEX(')', PersonName) - CHARINDEX('(', PersonName)-.5) as NickName
from Person;

/**********************

QUESTION 6

Write a query to return risk data for all patients, all payers 
and a moving average of risk for that patient and payer in dbo.Risk. 

**********************/

select distinct PersonID, 
AttributedPayer, 
AVG(RiskScore) OVER (PARTITION BY PersonID ORDER BY RiskDateTime) AS MovingAvg
from Risk;




