from datatest import check_for_nulls
from datatest import check_for_min_max
from datatest import check_for_valid_values
from datatest import check_for_duplicates

from time import time,ctime


test1={
	"testname":"Check for nulls",
	"test":check_for_nulls,
	"column": "firstname",
	"table": "demo"
}


test2={
	"testname":"Check for min and max",
	"test":check_for_min_max,
	"column": "riskq1",
	"table": "qrtrsk",
	"minimum":0,
	"maximum":1
}


test3={
	"testname":"Check for valid values",
	"test":check_for_valid_values,
	"column": "sex",
	"table": "demo",
	"valid_values":{'M','F'}
}


test4={
	"testname":"Check for duplicates",
	"test":check_for_duplicates,
	"column": "id",
	"table": "demo"
}

test5={
	"testname":"Check for nulls",
	"test":check_for_nulls,
	"column": "id",
	"table": "qrtrsk"
}

test6={
	"testname":"Check for min and max",
	"test":check_for_min_max,
	"column": "riskq2",
	"table": "qrtrsk",
	"minimum":0,
	"maximum":1
}

test7={
	"testname":"Check for valid values",
	"test":check_for_valid_values,
	"column": "attributedq1",
	"table": "qrtrsk",
	"valid_values":{'Yes','No'}
}

test8={
	"testname":"Check for duplicates",
	"test":check_for_duplicates,
	"column": "id",
	"table": "qrtrsk"
}
