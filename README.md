# Data Engineering Assessment
This repository contains the scripts and sample data necessary to complete Privia's Data Engineering Technical Assessment.

# Jeremy Hess, 4/18/2021, Data Engineering Assessment

## I have included all of my .py files, and as you can see, updated the readme file, please see my notes below

## This is the third time I have ever written Python code.  You will have to assess whether I can learn it over time.
* Fortunately, I have learned Java and SAS and it feels like a combination of the two, so I was able to put something together
* I believe I have met all of the requirements, except the Unit Testing.  I don't have experience in this area.
* Again, I am a believer in Test Driven Development and willing to learn.
* I also would need to review a style guide and learn the best practices for a coding style in Python

## What users need to know
* Just open the main file
* At the top you will enter everything that the program needs.
* Please enter the file path, file name, and the sheet that contains the information you would like to prepare.

## Test vs Real Life
* In the work place, I would also create way to pass connection information to the script
* On my home laptop, I have MYSQLEXPRESS instead of commercial SQL Server and it is on my laptop
* The MYSQLEXPRESS installation is using windows authentication, so for brevity, I just told the script as much
* Again, in the work place, I would build a way to pass confidential connection information to the script, not hard code

## Module Information
* main - To execute this, you can just open the main module, enter the information needed at the top of the code and the press RUN
* fileUploaders - takes the file path, file name, sheet name, uploads the file, gathers the meta data and adds it to the data
* extractors - breaks the data into two sets, the demographic and the risk attribution data sets
* curators - cleanses the data and transposes it, if needed
* tbl_creators - checks for the table in the sql database, if it doesn't exist, then it creates the table
* sqlDataLoaders - loads the demographic and risk attribution data into the respective sql tables



## Prerequsites - have all been met by JH, also installed PyCharm and used it for my IDE

### Database
* Local installation of Microsoft SQL Server 2012 or higher. 
    * *You may use another Database Platform if necessary, but please note that sample scripts are written for SQL Server.*
* SQL Server Management studio or another SQL client

#### Installing the Sample Data
* Run the PersonDatabase.sql script to create and insert data into the PersonDatabase.
    * If not using SQL Server, this script may need to be altered.
* Import the dbo.Contracts.txt flat file data to a table into the PersonDatabase to answer Question 9.

### Coding
* Local Installation of Python 3.6 or Higher
    * *You may use another object-oriented programming language if necessary.*

### Submitting Answers
Please fork this repository and submit your answers for review via a GitHub pull request.

