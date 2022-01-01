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

--I use a CTE to rank rows in risk table by riskdatetime.  I use a left join in order to include all persons, including those without a match in Risk table.  I limit to RN = 1 to get most recent risklevel only.
  ;WITH cte AS
  (
  SELECT	[PersonID]
			,[RiskLevel] 
			,rank() over (partition by personid order by riskdatetime desc) as rn
  FROM		[Risk]
  )

  SELECT	p.[PersonName]
			,c.[RiskLevel]
  FROM		[Person] p
  LEFT JOIN	cte c
	ON		p.[PersonID] = c.[PersonID]
	AND		rn = 1


/**********************

QUESTION 2


The table dbo.Person contains basic demographic information. The source system users 
input nicknames as strings inside parenthesis. Write a query or group of queries to 
return the full name and nickname of each person. The nickname should contain only letters 
or be blank if no nickname exists.

**********************/

--Use charindex to find position of open and close parenthesis.  However, if no parenthesis are present it will throw an error, so a case statement is needed to first check if parenthesis are present.
SELECT	PERSONNAME
--			,charindex('(', personname) as open_pos
--			,charindex(')', personname) as close_pos
--			,charindex(')', personname) - charindex('(', personname)-1 as name_length
		,case when charindex('(', personname) < 1 then personname
			--replace nickname (from code below) with '', then replace ) with '', then repalce double spaces w/ single space.
			else ltrim(rtrim(replace(replace(replace(personname, substring(personname, charindex('(', personname), charindex(')', personname) - charindex('(', personname)+1),'') ,')' ,''),'  ', ' '))) end as FullName
		,case when charindex('(', personname) < 1 then ''
			--substring(personname, open paren location, length of nickname (close position - open position) 
			else	substring(personname, charindex('(', personname)+1, charindex(')', personname) - charindex('(', personname)-1)
			end as NICKNAME
FROM [Person]


/**********************

QUESTION 6

Write a query to return risk data for all patients, all payers 
and a moving average of risk for that patient and payer in dbo.Risk. 

**********************/

--Do you want all patient and payer risk date in one table?  Is the moving average for a patient+payer pair?
select	PersonID
		,AttributedPayer
		,RiskLevel
		,RiskScore
		,RISKDATETIME
		--,AVG(RiskScore) OVER (PARTITION BY PersonID ORDER BY RISKDATETIME ASC ROWS 1 PRECEDING) AS PatientMovingAverage
		--,AVG(RiskScore) OVER (PARTITION BY attributedpayer, AttributedPayer ORDER BY RISKDATETIME ASC ROWS 1 PRECEDING) AS PayerMovingAverage
		,AVG(RiskScore) OVER (PARTITION BY PersonID, AttributedPayer ORDER BY RISKDATETIME ASC ROWS 1 PRECEDING) AS PatientPayerMovingAverage
FROM	RISK
order by PersonID, AttributedPayer, RiskDateTime


