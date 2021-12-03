USE PERSONDATABASE

/*********************
Hello! 

Please use the test data provided in the file 'PersonDatabase' to answer the following
questions. Please also import the dbo.Contacts flat file to a table for use. 

All answers should be executable on a MS SQL Server 2012 instance.

I have no access to run TSQL in my home, and I do not have a microsoft license to virtualize anything. I would have liked
to follow the standards, it just was not possible currently.
***********************



QUESTION 1

The table dbo.Risk contains calculated risk scores for the population in dbo.Person. Write a 
query or group of queries that return the patient name, and their most recent risk level(s). 
Any patients that dont have a risk level should also be included in the results.
**********************/


select p.personname, r.riskscore
from risk as r right join person as p
on r.personid = p.personid
order by 1,2;


/**********************

QUESTION 2


The table dbo.Person contains basic demographic information. The source system users 
input nicknames as strings inside parenthesis. Write a query or group of queries to 
return the full name and nickname of each person. The nickname should contain only letters 
or be blank if no nickname exists.

**********************/
select trim(leading '(' from (substring(personname, (position('(' in personname)), ((position(')'in personname) - (position('(' in personname))))))) as nickname,
trim(trailing ')' from replace(personname, concat('(',trim(leading '(' from (substring(personname, (position('(' in personname)), ((position(')'in personname) - (position('(' in personname))))))),')'), '')) as FullName
from person
order by FullName, nickname;

/**********************

QUESTION 6

Write a query to return risk data for all patients, all payers 
and a moving average of risk for that patient and payer in dbo.Risk. 

**********************/


SELECT risk.personid,	attributedpayer,	riskscore,	risklevel,	riskdatetime,	personname,
      		avg(riskscore) OVER(PARTITION BY person.personname, attributedpayer ORDER BY riskdatetime ROWS BETWEEN 5 PRECEDING AND CURRENT ROW) AS three_day_moving_average
FROM risk left join person
on person.personid = risk.personid;


