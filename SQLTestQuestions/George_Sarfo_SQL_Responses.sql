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

--use window function rank to get recent riskscores, 
--if recent different riskscores occur at the same time return both

select PersonName, RiskScore, riskdatetime, 
rank() over(partition by ri.personid order by ri.riskdatetime desc) as RecentRiskScore
from dbo.person as per left join 
dbo.Risk as ri on per.PersonID=ri.PersonID
order by PersonName, RiskDateTime desc




/**********************

QUESTION 2


The table dbo.Person contains basic demographic information. The source system users 
input nicknames as strings inside parenthesis. Write a query or group of queries to 
return the full name and nickname of each person. The nickname should contain only letters 
or be blank if no nickname exists.

**********************/


--use charindex to find position of ( and ) and use substring to extract nicknames, 
--replace (, ) and nicknames and with '' empty string to get full name with no nickname

select 
personname as fullname_with_nickname,
REPLACE(REPLACE(REPLACE(personname, '('+nickname+')', ''), '(', ''), ')', '') as fullname_no_nickname, nickname
from
(
select personname, case when (personname like '%(%' and personname like '%)%')
then
  substring(Personname, CHARINDEX('(', personname, 1)+1, (-1 + CHARINDEX(')', personname, 1) - CHARINDEX('(', personname, 1))) 
 else '' end as nickname
 from dbo.Person
)q

/**********************

QUESTION 6

Write a query to return risk data for all patients, all payers 
and a moving average of risk for that patient and payer in dbo.Risk. 

**********************/

--moving average can be calculated at multiple levels
--patient level, payer level or even patient-payer combo level
--moving avg is calculated for past 5 days and now (this can be parameterized)

select per.PersonName, ri.AttributedPayer, Riskscore, riskdatetime,

AVG(RiskScore) OVER (PARTITION BY personname
ORDER BY RiskDateTime
ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
) Patient_Level_FiveDay_RiskMovingAvg,

AVG(RiskScore) OVER (PARTITION BY attributedpayer
ORDER BY RiskDateTime
ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
) Payer_Level_FiveDay_RiskMovingAvg,

AVG(RiskScore) OVER (PARTITION BY personname, attributedpayer
ORDER BY RiskDateTime
ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
) Patient_cum_Payer_Level_FiveDay_RiskMovingAvg
from dbo.person as per 
left join dbo.Risk as ri
on per.PersonID = ri.PersonID
order by personname, RiskDateTime





