USE PERSONDATABASE

-- Imported dbo.Contacts using import flat file wizard



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
select p.PersonName, r.RiskLevel from (
   select r.PersonID, min(r.RiskDateTime) as MinRiskTime 
     from dbo.Risk r 
    group by r.PersonID
	) m
  join dbo.Person p on m.PersonID = p.PersonID
left join dbo.Risk r on r.PersonID = m.PersonID and r.RiskDateTime = m.MinRiskTime;



/**********************
QUESTION 2
The table dbo.Person contains basic demographic information. The source system users 
input nicknames as strings inside parenthesis. Write a query or group of queries to 
return the full name and nickname of each person. The nickname should contain only letters 
or be blank if no nickname exists.
**********************/
--right(PersonName, LEN(PersonName) - CHARINDEX(')', PersonName))
--
with 
FullName (fullname, PersonID) as (
   select (left(PersonName, CHARINDEX('(', PersonName) - 1)  + reverse(left(reverse(PersonName), charindex(')', reverse(PersonName)) -1))) as fullname, PersonID
     from dbo.Person
    where PersonName like '%(%' and PersonName like '%)%'
	),
NickName (nickname, PersonID) as (
   select SUBSTRING(PersonName,CHARINDEX('(', PersonName) + 1,CHARINDEX(')', PersonName) - CHARINDEX('(', PersonName) - 1) as nickname, PersonID
     from dbo.Person
    where PersonName like '%(%' and PersonName like '%)%'
	)

select COALESCE(fullname, PersonName) as FullName, COALESCE(nickname, '') as NickName
  from FullName
  join NickName on FullName.PersonID = NickName.PersonID
right join dbo.Person on dbo.Person.PersonID = FullName.PersonID;



/**********************
QUESTION 6
Write a query to return risk data for all patients, all payers 
and a moving average of risk for that patient and payer in dbo.Risk. 
**********************/
select p.PersonName, r.*, a.AverageRisk
  from dbo.Person p 
  join dbo.Risk r on p.PersonID = r.PersonID 
  join (
        select PersonID, avg(RiskScore) as AverageRisk
		  from dbo.Risk
		 group by PersonID
	   ) a on p.PersonID = a.PersonID;