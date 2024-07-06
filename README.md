# BE_PARKFINITE
### PLEASE UPDATE THIS README TO REFLECT CURRENT STATE OF PROJECT BEFORE PUSHING TO GIT
#
### PROJECT SETUP:
# Initiate a virtual environament and reference requirements.txt to install necessary project dependencies:
# In your CLI 
#       1/ Create virtual enivorment in the project root folder (/be_parkfinite) - run 'python3 -m venv venv'
#       2/ Activate your virtual environment - run 'source venv/bin/activate' 
#       3/ Install project dependencies - run 'pip install -r requirements.txt'
#
### RUNNING THE APP:
* Run the app locally:
*       run 'uvicorn main:App' to run the app on http://127.0.0.1:8000
*       run 'pytest' to execute all avaiable test suites
*      
*
*         
### IF THE APP OR TESTING WONT RUN:
* Ensure your pythonpath is set correctly via an ABSOLTE FILE PATH TO THE PROJECT ROOT FOLDER (/be_parkfinite):
* In your CLI:
*        1/ run 'echo $PYTHONPATH'
*        2/ If there is no set pythonpath then a workaraound is to set it manually: 
*               run 'export PYTHONPATH="/path/to/poject/be_parkfinite:$PYTHONPATH"'
*        3/ To avoide having to run this command every time you activate your venv: 
*               add a command to the relevant venv/bin/activate file for the operating system you are on.
*
*
*
### AVAILABLE TESTING COMMANDS:
* In your CLI:
*       use 'pytest -m main' to run main api test suite, for main.py endpoints
*      use 'pytest -m db_utils' to run database utilities test suite
*       use 'pytest -m test_utils' to run testing utilities test suite
*
*
*
### DEVELOPMENT AND PRODUCITON DATABASES:
* SETUP .ENV FILES LOCALLY:
* In order to seed either the develeopment or production database you will need to set up .env files locally
* --PLEASE ADD THESE .ENV FILES TO GIT IGNORE TO KEEP THE DATABASES SECURE!!--
*       add .env.development. containing the line 'DATABASE_URL=sqlite:///../dev.db'. This will create a local dev db.
*       add .env.production, containing the line 'DATABASE_URL=postgresql://PATH/TO/PRODUCTION/DB/INCLUDING/PASSWORD/
*
### SEED SPECIFIED DATABASE:
* In your CLI:
*       run 'ENV=development python3 seed.py':
*       replace 'development' with 'production' to seed the hosted Postgres production db
* 
### NOTE: BOTH DATABASES ARE CURRENTLY SEEDED FROM THE SAME DEVELOPMENT DATA FILE!