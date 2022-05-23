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

with t2 as (select per.personid,per.personname,rs.risklevel,rs.riskdatetime , ROW_NUMBER() OVER ( partition by per.personid,rs.riskdatetime ORDER BY RiskDateTime DESC) AS ID from dbo.person per left join dbo.risk rs on per.personid=
rs.personid),
t3 as (
select t2.* from t2 as t1 inner join t2 as t2 on t1.PersonID=t2.PersonID and t1.id>1 and t1.RiskDateTime=t2.RiskDateTime
 ) 
 select t3.personid,t3.personname,t3.risklevel,t3.riskdatetime from t3 
 union
 select b.personid,b.personname,b.risklevel,b.riskdatetime from (
 select t2.*, ROW_NUMBER() OVER ( partition by t2.personid ORDER BY RiskDateTime DESC) AS ID1 from t2 where t2.personid not in (select distinct personid from t3)) b
 where b.ID1=1




/**********************

QUESTION 2


The table dbo.Person contains basic demographic information. The source system users 
input nicknames as strings inside parenthesis. Write a query or group of queries to 
return the full name and nickname of each person. The nickname should contain only letters 
or be blank if no nickname exists.

**********************/

use persondatabase;

with abc as (
select personName,
(CHARINDEX('(',personName)+1) as p1,
(CHARINDEX(')',personName)) as p2 
from dbo.Person 
)
select  
case when (p2-p1)=0 then ''
 when (p2-p1)=-1 then ''
else substring(personname,p1,p2-p1)
end as nickname ,personname
from abc 
where (p2-p1)>=-1;

/**********************

QUESTION 6

Write a query to return risk data for all patients, all payers 
and a moving average of risk for that patient and payer in dbo.Risk. 

**********************/

select avg(riskscore) as Moving_avergae,per.PersonID
--,AttributedPayer  
from dbo.person per left join dbo.risk rs on per.personid=
rs.personid
group by per.PersonID

select avg(riskscore) as Moving_avergae
--,per.PersonID
,AttributedPayer  
from dbo.risk rs  left join dbo.person per on per.personid=
rs.personid
group by AttributedPayer


select avg(riskscore) as Moving_avergae,PersonID,AttributedPayer from dbo.risk
group by PersonID,AttributedPayer

/**********************
