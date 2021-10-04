
select PersonName, Iif(Len(nn)<2,null,nn) NickName, Trim(Replace(Replace(personName, Concat('(',nn,')') ,''),'  ','')) FullName
from Person
cross apply (values(SUBSTRING(PersonName, CHARINDEX('(', PersonName) +1,(((LEN(PersonName))-CHARINDEX(')',REVERSE(PersonName)))-CHARINDEX('(',PersonName))) ))c(nn)

