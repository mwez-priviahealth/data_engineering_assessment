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

SELECT ['Patient Name'], ['Risk Level'], ['Risk DateTime'] FROM (
  SELECT 
	  ['Patient Name'] = PersonName,
	  ['Risk Level'] = RiskLevel,
	  ['Risk DateTime'] = RiskDateTime,
	  ['DenseRank'] = DENSE_RANK() OVER (PARTITION BY PersonName ORDER BY RiskDateTime DESC)
  FROM dbo.Person LEFT JOIN dbo.Risk ON Person.PersonID = Risk.PersonID
) rank_table WHERE ['DenseRank'] = 1



/**********************

QUESTION 2


The table dbo.Person contains basic demographic information. The source system users 
input nicknames as strings inside parenthesis. Write a query or group of queries to 
return the full name and nickname of each person. The nickname should contain only letters 
or be blank if no nickname exists.

**********************/
	CREATE FUNCTION dbo.ExtractNickName (@raw_name VARCHAR(500))
	RETURNS VARCHAR(250)
	AS BEGIN
		DECLARE @result VARCHAR(250)

		IF (CHARINDEX('(', @raw_name) > 0 OR CHARINDEX(')', @raw_name) > 0) --Only parse if parens are in the name
			BEGIN
				SET @result = SUBSTRING(@raw_name,CHARINDEX('(', @raw_name) + 1,
													  CHARINDEX(')', @raw_name) - CHARINDEX('(', @raw_name) - 1)
			END
		ELSE
			BEGIN
				SET @result = NULL
			END

		RETURN @result

	END

	CREATE FUNCTION dbo.ExtractFullName (@raw_name VARCHAR(500))
	RETURNS VARCHAR(500)
	AS BEGIN
		DECLARE @result VARCHAR(500)
		DECLARE @nickname VARCHAR(250)

		SET @nickname = dbo.ExtractNickName(@raw_name)

		IF (@nickname IS NOT NULL) -- If there is a nickname, then we'll need to remove it.
			BEGIN
				SET @result = REPLACE(@raw_name, '(' + @nickname + ')', '')
				-- Handle any remaining parens
				SET @result = REPLACE(@result, '(','')
				SET @result = REPLACE(@result, ')','')
			END
		ELSE
			BEGIN
				SET @result = @raw_name
			END

		RETURN TRIM(@result)
	END

SELECT 
	[OriginalName] = PersonName,
	[Full Name] = dbo.ExtractFullName(PersonName),
	[NickName] = CASE 
						WHEN dbo.ExtractNickName(PersonName) = '' THEN NULL --Empty Nicknames will be changed to NULL
						ELSE dbo.ExtractNickName(PersonName)
					END
FROM dbo.Person


/**********************

QUESTION 6

Write a query to return risk data for all patients, all payers 
and a moving average of risk for that patient and payer in dbo.Risk. 

**********************/


SELECT 
	  [Patient Name] = PersonName,
	  [Payer] = AttributedPayer,
	  [Risk Score] = RiskScore,
	  [Risk DateTime] = RiskDateTime,
	  [MovingAverage] = AVG(RiskScore) OVER (PARTITION BY Person.PersonID, AttributedPayer ORDER BY RiskDateTime ASC)
  FROM dbo.Person LEFT JOIN dbo.Risk ON Person.PersonID = Risk.PersonID

