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

QUESTION 2


The table dbo.Person contains basic demographic information. The source system users 
input nicknames as strings inside parenthesis. Write a query or group of queries to 
return the full name and nickname of each person. The nickname should contain only letters 
or be blank if no nickname exists.

**********************/

/*Check the position of Open and Close Paranthesis*/
SELECT PersonName, CHARINDEX('(', PersonName), CHARINDEX( ')', PersonName)
FROM Person;

/**/
SELECT	PersonName,
    CASE
        WHEN CHARINDEX('(', PersonName) > 0 THEN
        CONCAT(
            SUBSTRING(PersonName, 1, CHARINDEX('(', PersonName) - 1 ),                   /* Searched string before "(" position */
            SUBSTRING(PersonName, CHARINDEX( ')', PersonName) + 1, LEN(PersonName))     /* Searched string after "(" position */
        )
        ELSE PersonName END AS FullName
        ,
    CASE
        WHEN CHARINDEX('(', PersonName) > 0 THEN
        SUBSTRING(PersonName, CHARINDEX('(', PersonName) + 1, (CHARINDEX( ')', PersonName) - (CHARINDEX('(', PersonName)) -1) )
        
        ELSE PersonName END AS NickName

FROM Person;

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
