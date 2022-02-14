
-- Answer for Question 1
/* The table dbo.Risk contains calculated risk scores for the population in dbo.Person. Write a 
query or group of queries that return the patient name, and their most recent risk level(s). 
Any patients that dont have a risk level should also be included in the results. */

SELECT 
  p.PersonName AS PatientName
, mr.RiskLevel AS MostRecentRiskLevel
FROM dbo.Person p
	outer apply
	(SELECT TOP 1
			RiskLevel
	   FROM dbo.Risk r
	  WHERE r.PersonId = p.PersonId 
	  ORDER BY RiskDateTime DESC
	) mr

--Answer for Question 2
/*The table dbo.Person contains basic demographic information. The source system users 
input nicknames as strings inside parenthesis. Write a query or group of queries to 
return the full name and nickname of each person. The nickname should contain only letters 
or be blank if no nickname exists.*/


SELECT
 CASE	
	WHEN CHARINDEX('(', PersonName) < 1 THEN PersonName -- No Nickname
	ElSE RTRIM(LTRIM(REPLACE(REPLACE(PersonName, SUBSTRING(PersonName, CHARINDEX('(', PersonName) , CHARINDEX(')', PersonName) - CHARINDEX('(', PersonName) + 1 ) , ''), ')', '')))
 END AS FullName
,CASE	
	WHEN CHARINDEX('(', PersonName) < 1 THEN null -- No Nickname
	WHEN CHARINDEX(')', PersonName ) - CHARINDEX('(', PersonName)  = 1 THEN null -- Empty Nickname
	ElSE SUBSTRING(PersonName, CHARINDEX('(', PersonName) + 1 , CHARINDEX(')', PersonName) - CHARINDEX('(', PersonName) - 1 ) 
  END as NickName
FROM  dbo.Person


--Question 6
/* Write a query to return risk data for all patients, all payers 
and a moving average of risk for that patient and payer in dbo.Risk. */

SELECT 
  r.AttributedPayer
, r.PersonID
, p.PersonName
, r.RiskScore
, r.RiskLevel
, r.RiskDatetime
, AVG(r.RiskScore) OVER(PARTITION BY r.PersonID,r.AttributedPayer ORDER BY r.RiskDateTime) AS RiskMovingAverage
FROM dbo.Risk r
     INNER JOIN dbo.Person p ON (r.PersonID = p.PersonID)
ORDER BY 
  r.AttributedPayer
, r.PersonId
, r.RiskDateTime





