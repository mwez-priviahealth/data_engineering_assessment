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

SELECT PersonName, RiskLevel
-- Writing subquery that orders each persons risk level by date descending 
-- DENSE_RANK() is used here because it assigns the same rank to equal time stamps 
-- which allows us to pull all of the most recent risk levels instead of one per person
FROM (SELECT p.*, dbo.Risk.RiskLevel, dbo.Risk.RiskDateTime, DENSE_RANK() 
-- Partitioning to order the records of each person by date and assign a row number to the record
OVER (PARTITION BY PersonName order by RiskDateTime desc) as rn
FROM dbo.Person p
FULL JOIN dbo.Risk ON p.PersonID = dbo.Risk.PersonID) m2
-- Selecting to show the most recent risk records
WHERE m2.rn = 1 

/**********************

QUESTION 2


The table dbo.Person contains basic demographic information. The source system users 
input nicknames as strings inside parenthesis. Write a query or group of queries to 
return the full name and nickname of each person. The nickname should contain only letters 
or be blank if no nickname exists.

**********************/


SELECT 
-- Trimming white space before and after full name and replacing both the nick name and parentheses with nothing
TRIM(REPLACE(REPLACE(PersonName, '('+NickName+')', ''), ')', '')) as FullName, NickName
FROM(
-- Creating subquery to pull nick name from each person's full name and setting it to the NickName column
SELECT PersonName, 
CASE WHEN (PersonName LIKE '%(%' AND personname LIKE '%)%')
	THEN SUBSTRING(PersonName, CHARINDEX('(', PersonName, 1)+1, (-1 + CHARINDEX(')', PersonName, 1) - CHARINDEX('(', PersonName, 1))) 
	ELSE '' 
	END AS NickName
	FROM dbo.Person
) as TEMP


/**********************

QUESTION 6

Write a query to return risk data for all patients, all payers 
and a moving average of risk for that patient and payer in dbo.Risk. 

**********************/

SELECT PersonName, AttributedPayer, RiskLevel, AVG(RiskScore)
-- Pulling the moving average risk score over the last 4 most recent scores
OVER (ORDER BY RiskDateTime DESC ROWS BETWEEN 3 PRECEDING AND CURRENT ROW)
as MovingAverage
FROM dbo.Person, dbo.Risk


