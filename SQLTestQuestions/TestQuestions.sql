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

SELECT PersonName, max(r.RiskLevel) AS RiskLevel
FROM dbo.Person AS p
LEFT JOIN dbo.Risk AS r
ON r.PersonID=p.PersonID
GROUP BY PersonName;

/**********************

QUESTION 2


The table dbo.Person contains basic demographic information. The source system users 
input nicknames as strings inside parenthesis. Write a query or group of queries to 
return the full name and nickname of each person. The nickname should contain only letters 
or be blank if no nickname exists.

**********************/

CREATE PROCEDURE nametable()

AS
BEGIN
SET NOCOUNT ON;

	SELECT Replace(Replace(PersonName,')',','),'(',',') AS Name, dbo.SUBSTRING_INDEX(dbo.SUBSTRING_INDEX(PersonName, '(', -1), ')', 1) AS NickName INTO #nametable5 FROM dbo.Person WHERE PersonName LIKE '%(%)%';

	SELECT PersonName INTO #nametable6 FROM dbo.person WHERE PersonName NOT LIKE '%(%)%';

	ALTER TABLE #nametable6 ADD COLUMN blank VARCHAR(4) NOT NULL;

	SELECT LTRIM(CONCAT(RTRIM(SUBSTRING_INDEX(name,',',1)), dbo.SUBSTRING_INDEX(name,',', -1),' ','')) as Name, Nickname INTO #nametable7 FROM nametable5;

	SELECT * INTO #nametable8 FROM nametable7 UNION SELECT * INTO #nametable8 FROM nametable6);

END; 
GO

CALL nametable();
/**********************

QUESTION 6

Write a query to return risk data for all patients, all payers 
and a moving average of risk for that patient and payer in dbo.Risk. 

**********************/


SELECT p.PersonName, r.RiskDateTime, r.RiskScore, avg(r.RiskScore) OVER(PARTITION BY p.PersonName ORDER BY RiskDateTime ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS MovingAveragePatientRisk, r.AttributedPayer, avg(r.RiskScore) OVER(PARTITION BY r.AttributedPayer, p.PersonID ORDER BY r.AttributedPayer, r.RiskDateTime ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS MovingAveragePayerRisk
FROM dbo.Person AS p
LEFT JOIN dbo.Risk AS r
ON r.PersonID=p.PersonID
ORDER BY p.PersonID, r.RiskDateTime;


