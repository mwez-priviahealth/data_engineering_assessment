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

WITH info (PersonName, RiskLevel, RiskRank, RiskDateTime) AS (
    SELECT PersonName, RiskLevel, Rank() OVER (PARTITION BY r.PersonID ORDER BY RiskDateTime DESC), RiskDateTime
    FROM Person p
    LEFT JOIN Risk r ON r.PersonID = p.PersonID
)
SELECT PersonName, RiskLevel
FROM info
WHERE RiskRank =1;




/**********************

QUESTION 6

Write a query to return risk data for all patients, all payers 
and a moving average of risk for that patient and payer in dbo.Risk. 

**********************/

SELECT
	PersonName,
	AttributedPayer AS Payer,
	RiskScore,
	RiskDateTime,
	AVG(RiskScore) OVER (PARTITION BY p.PersonID, AttributedPayer ORDER BY RiskDateTime ASC) AS MovingAverage
  FROM Person p
  LEFT JOIN Risk r
  ON p.PersonID = r.PersonID
