# ETL (Python) Assignment
***
The purpose of this assignment is:

1. ETL(Extract, transform, load) job that consumes an API endpoint 
(in this case, Dota’s Public API)
2. Builds a few KPIs (key performance indicators) that allows us to analyse
relevant statistical data regarding said subject.
3. Application logging the KPIs information of a player, properly
serialized as JSON messages (where float values represented in double-precision
floating-point format), like the following example:
{
"game": "Dota",
"player_name": "YrikGood1",
"total_games": 7,
"task_duration": "5.75 sec",
"max_kda": 18.0,
"min_kda": 0.0,
"avg_kda": 6.32,
"max_kp": "77.78%",
"min_kp": "0.00%",
"avg_kp": "61.66%"
}
4. Application logging errors:
* Example 1
    {
    "code": 400,
    "message": "Bad Request! Please check input json parameters."
    }
* Example 2
    {
    "code": 404,
    "message": "Page not found! Please check url. Example: ../players/top?count=11"
    }
5.  Finally, application log the number of games and the duration of the
task. (see above JSON log message in point 3 (total_games, task_duration))

## Table of Contents
1. [General Info](#general-info)
2. [Frameworks](#frameworks)
3. [Files](#project-files)
3. [Notes](#notes)

## General Info
***
To get the top 11 (count) of current player (KPI's) by 'account_id' and 'name'
you need to send below POST request with below JSON body:

IP_ADDRESS:5000/players/top?count=11

{
"account_id": 639740,
"name": "YrikGood1"
}

IP_ADDRESS will be generated from AWS Fargate cluster service.
# The IP_ADDRESS will be provided via Email.
# Note: The AWS Fargate cluster working on hourly payment.
! PLEASE INFORM ME WHEN YOU FINISH THE TESTING TO STOP THE AWS FARGATE CLUSTER.


## Frameworks
***
The application developed with the following tools and services:

1. Python
2. Docker (for containerizing the application)
3. Github (https://github.com/karbag89/python_etl)
4. Gitlab CI pipeline (https://gitlab.com/karbag89/python_etl)
5. AWS Fargate cluster ()


## Project Files
***
1. Python files:
    * main.py
    * controller.py
    * error.py
    * test_controller.py
2. Requirements text file:
    * requirements.txt
3. Docker files:
    * Dockerfile
    * .dockerignore
4. Gitlab CI file:
    * .gitlab-ci.yml
5. ReadMe file:
    * README.md

# Note. The flake8 library was used for above all Python files to fit the (PEP8)
# style guide for Python code.
# Note: The pytest library was used for testing.


## Notes
***
1. If user input top n match value is less then 1, we set the value to default
   10.
2. If count of matches is less than as user input top n match value,
   then we set the count value to maximum matches count.
