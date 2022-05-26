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
SELECT p.PersonName, r.RiskLevel
FROM PersonDatabase.dbo.Person p 
LEFT JOIN (SELECT PersonID, RiskLevel
	   FROM (SELECT PersonID, RiskLevel, DENSE_RANK() OVER(PARTITION BY PersonID ORDER BY RiskDateTime DESC) AS rnk
		 FROM PersonDatabase.dbo.Risk) a
		 WHERE rnk = 1) r
ON p.PersonID = r.PersonID


/**********************

QUESTION 2


The table dbo.Person contains basic demographic information. The source system users 
input nicknames as strings inside parenthesis. Write a query or group of queries to 
return the full name and nickname of each person. The nickname should contain only letters 
or be blank if no nickname exists.

**********************/
SELECT CASE WHEN CHARINDEX('(', PersonName)+CHARINDEX(')', PersonName) > 0 
	    THEN TRIM(LEFT(PersonName, IIF(CHARINDEX('(', PersonName) = 0, 0, CHARINDEX('(', PersonName)-1))+RIGHT(PersonName, IIF(LEN(PersonName)-CHARINDEX(')', PersonName) = 0, 0, LEN(PersonName)-CHARINDEX(')', PersonName)-1)))
	    ELSE PersonName
       END AS FullName,
       NULLIF(CASE WHEN CHARINDEX('(', PersonName)+CHARINDEX(')', PersonName) > 0 
		   THEN SUBSTRING(PersonName, CHARINDEX('(', PersonName)+1, CHARINDEX(')', PersonName)-1-CHARINDEX('(', PersonName)) 
		   ELSE NULL
	      END, '') AS NickName
FROM PersonDatabase.dbo.Person


/**********************

QUESTION 6

Write a query to return risk data for all patients, all payers 
and a moving average of risk for that patient and payer in dbo.Risk. 

**********************/
SELECT p.PersonName, r.AttributedPayer, r.RiskScore, AVG(r.RiskScore) OVER(PARTITION BY r.PersonID, r.AttributedPayer ORDER BY r.RiskDateTime) AS Moving_Average
FROM PersonDatabase.dbo.Person p 
LEFT JOIN PersonDatabase.dbo.Risk r
ON p.PersonID = r.PersonID



