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
-- i had to add Riskscore on order by for row rank as Personid 1 has silver and bronze risklevel on same timestamp
USE PersonDatabase
SELECT PersonName, RiskLevel
FROM   [dbo].[Person] p
LEFT JOIN  
      (
	   SELECT PersonID, 
       RiskLevel,
       Row_number() over(partition by PersonID order by RiskDateTime desc, RiskScore desc) as RowRank
       FROM   [dbo].[Risk]

	  ) RISK
ON p.Personid=risk.Personid and risk.RowRank=1




/**********************

QUESTION 2


The table dbo.Person contains basic demographic information. The source system users 
input nicknames as strings inside parenthesis. Write a query or group of queries to 
return the full name and nickname of each person. The nickname should contain only letters 
or be blank if no nickname exists.

**********************/
SELECT  [PersonName]
		,CASE WHEN  CHARINDEX(')',[PersonName])>0 and   CHARINDEX('(',[PersonName])>0 THEN 
		    concat(Substring([PersonName],1,CHARINDEX('(',[PersonName])-1),Substring([PersonName],CHARINDEX(')',[PersonName])+1,len([PersonName])-CHARINDEX(')',[PersonName])))
			ELSE [PersonName] END AS FullName

	    ,REPLACE (
		  REPLACE(CASE WHEN  CHARINDEX(')',[PersonName])>0 and   CHARINDEX('(',[PersonName])>0
		  THEN SUBSTRING ([PersonName],CHARINDEX('(',[PersonName])+1,CHARINDEX(')',[PersonName])-CHARINDEX('(',[PersonName])-1)
		  ELSE '' END,')',''
		        ),'(',''
		  ) AS NickName
   
FROM [dbo].[Person]


/**********************

QUESTION 6

Write a query to return risk data for all patients, all payers 
and a moving average of risk for that patient and payer in dbo.Risk. 

**********************/


SELECT  [PersonID]
      ,[AttributedPayer]
      ,[RiskScore]
      ,[RiskLevel]
      ,[RiskDateTime]
	  ,AVG(RiskScore) OVER(PARTITION BY PERSONID ,AttributedPayer ORDER BY RiskDateTime) AS MV_PerPatientandPayer
  FROM [dbo].[Risk]

