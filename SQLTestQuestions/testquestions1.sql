/*********************

QUESTION 1

The table dbo.Risk contains calculated risk scores for the population in dbo.Person. Write a 
query or group of queries that return the patient name, and their most recent risk level(s). 
Any patients that dont have a risk level should also be included in the results. 

**********************/

SELECT PersonName, max(r.RiskLevel) AS RiskLevel
FROM Person AS p
LEFT JOIN Risk AS r
ON r.PersonID=p.PersonID
GROUP BY PersonName;

/**********************

QUESTION 2


The table dbo.Person contains basic demographic information. The source system users 
input nicknames as strings inside parenthesis. Write a query or group of queries to 
return the full name and nickname of each person. The nickname should contain only letters 
or be blank if no nickname exists.

**********************/

DELIMITER //

CREATE PROCEDURE nametable()

BEGIN

	CREATE TEMPORARY TABLE nametable5
	(SELECT Replace(Replace(PersonName,')',','),'(',',') AS Name, SUBSTRING_INDEX(SUBSTRING_INDEX(PersonName, '(', -1), ')', 1) AS NickName FROM Person WHERE PersonName LIKE '%(%)%');

	CREATE TEMPORARY TABLE nametable6
	(SELECT PersonName FROM person WHERE PersonName NOT LIKE '%(%)%');

	ALTER TABLE nametable6
	ADD COLUMN blank VARCHAR(4) NOT NULL AFTER PersonName;

	CREATE TEMPORARY TABLE nametable7
	(SELECT LTRIM(CONCAT(RTRIM(SUBSTRING_INDEX(name,',',1)), SUBSTRING_INDEX(name,',', -1),' ','')) as Name, Nickname FROM nametable5);

	CREATE TEMPORARY TABLE nametable8
	(SELECT * FROM nametable7 UNION SELECT * FROM nametable6);

END; //

DELIMITER ;

CALL nametable();

/**********************

QUESTION 6

Write a query to return risk data for all patients, all payers 
and a moving average of risk for that patient and payer in dbo.Risk. 

**********************/


SELECT p.PersonName, r.RiskDateTime, r.RiskScore, avg(r.RiskScore) OVER(PARTITION BY p.PersonName ORDER BY RiskDateTime ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS MovingAverageRisk, r.AttributedPayer
FROM Person AS p
LEFT JOIN Risk AS r
ON r.PersonID=p.PersonID
ORDER BY p.PersonID, r.RiskDateTime;