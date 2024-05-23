@echo off

set /p id=Enter your everytime ID: 
set /p pw=Enter your everytime password: 
set /p apikey=Enter your API key: 
set /p assistkey=Enter your Assistant key: 

cd Server

echo ID=%id%> .env
echo PW=%pw%>> .env
echo OPENAI_API_KEY=%apikey%>> .env
echo OPENAI_ASSISTANT_KEY=%assistkey%>> .env

echo .env file created successfully.
pause