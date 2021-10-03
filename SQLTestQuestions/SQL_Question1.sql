--Selecting relevant fields
Select 
Risk.PersonID
,Person.PersonName
,Risk.RiskLevel
,Risk.RiskDateTime
From dbo.Risk
--getting the max date per personID
inner join 
(
	Select PersonID, max(RiskDateTime) as MaxDate
	from dbo.Risk
	Group by PersonID
) 
rm on Risk.PersonID = rm.PersonID and Risk.RiskDateTime = rm.MaxDate
--Join person table
full join dbo.Person
on Person.PersonID = Risk.PersonID



