@echo off

echo Installing pipenv... & pip install --upgrade pipenv
     echo Installing dependencies
     pipenv run pip install -r requirements.txt & pipenv run python script.py
start "" "grouped"
 pause
