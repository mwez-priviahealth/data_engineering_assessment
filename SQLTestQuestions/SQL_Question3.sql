Select 
Risk.PersonID
,Risk.AttributedPayer
,Risk.RiskDateTime
,avg(Risk.RiskScore) OVER
(
	Partition by Risk.AttributedPayer
	ORDER by Risk.RiskDateTime 
	Rows between 2 preceding and current row) --This is where I'm stuck. Having trouble grouping by personID and Payer and averaging over a different amount of rows depending on the number of instances of a payer
	as moving_average

from dbo.Risk
where PersonID = '1' 

Select 
Risk.PersonID
,Risk.AttributedPayer
,Risk.RiskDateTime
,avg(Risk.RiskScore) OVER
(
	Partition by Risk.AttributedPayer
	ORDER by Risk.RiskDateTime 
	Rows between 1 preceding and current row)
	as moving_average

from dbo.Risk
where PersonID = '2' 

Select 
Risk.PersonID
,Risk.AttributedPayer
,Risk.RiskDateTime
,avg(Risk.RiskScore) OVER
(
	Partition by Risk.AttributedPayer
	ORDER by Risk.RiskDateTime 
	Rows between 1 preceding and current row)
	as moving_average

from dbo.Risk
where PersonID = '4' 

Select 
Risk.PersonID
,Risk.AttributedPayer
,Risk.RiskDateTime
,avg(Risk.RiskScore) OVER
(
	Partition by Risk.AttributedPayer
	ORDER by Risk.RiskDateTime 
	Rows between 1 preceding and current row)
	as moving_average

from dbo.Risk
where PersonID = '5' 
