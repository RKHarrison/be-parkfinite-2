# BE_PARKFINITE
### PLEASE UPDATE THIS README TO REFLECT CURRENT STATE OF PROJECT BEFORE PUSHING TO GIT

### PROJECT SETUP:
Initiate a virtual environament and reference requirements.txt to install necessary project dependencies:
* Create virtual enivorment in the project root folder (/be_parkfinite):
In your CLI, navigate to the project root folder and run: 
*      python3 -m venv venv
* Activate your virtual environment:
In your CLI run:
*       source venv/bin/activate
* Install project dependencies:
In your CLI run:
*       pip install -r requirements.txt


## RUNNING THE APP:
* Run the app locally on http://127.0.0.1:8000:
In your CLI run:
*       uvicorn main:app
* To execute all avaiable test suites:
In your CLI run:
*       pytest       
### IF THE APP OR TESTING WONT RUN:
* Ensure your pythonpath is set correctly via an ABSOLTE FILE PATH TO THE PROJECT ROOT FOLDER (/be_parkfinite):
In your CLI run:
*       echo $PYTHONPATH
* If there is no set pythonpath then a workaraound is to set it manually: 
*       export PYTHONPATH="/path/to/poject/be_parkfinite:$PYTHONPATH"
* To avoid having to run this command every time you activate your venv: 
add a command to the relevant venv/bin/activate file for the operating system you are on.
### AVAILABLE TESTING COMMANDS:
In your CLI:
* To run main api test suite, for main.py endpoints:
*      pytest -m main
* To run database utilities test suite:
*      pytest -m db_utils
* To run testing utilities test suite:
*      use 'pytest -m test_utils' 

## DEVELOPMENT AND PRODUCITON DATABASES:
--PLEASE ADD .ENV FILES TO GIT IGNORE TO KEEP THE DATABASES SECURE!!--
--PLEASE ADD ANY LOCALLY STORED SQLITE DATABASE TO GITIGNORE TOO!--
### Setup .env.development and .env.production in be_parkfinite/api/:
* To create and seed a locally stored SQLite development database add a .env.development file containing the line:
*      DATABASE_URL=sqlite:///../dev.db
-Remember to add this file to .gitignore-
* To seed to the hosted production database add a .env.production file containing the following line:
*      DATABASE_URL=postgresql://PATH/TO/PRODUCTION/DB/INCLUDING/PASSWORD/
### SEED SPECIFIED DATABASE:
In your CLI run:
*      ENV=development python3 seed.py
replace 'development' with 'production' to seed the hosted Postgres production db.

## Seeding the Database
### Overview
When seeding the database with user data for testing or development, we use pre-hashed passwords to speed up the process. These passwords have been pre-hashed using our utility function and are stored directly in the seed data.
### Generating a New Pre-Hashed Password
If you need to generate a new pre-hashed password (for example, if you are setting up a new local repository or updating the seed data), follow these steps:

1. Open a Python shell within the project's virtual environment.
2. Run the following commands to generate the hash:

    ```python
    from api.utils.security_utils.password_utils import hash_password
    print(hash_password('your_password_here')
    ```

3. Replace the old pre-hashed password in yourr .env.pre_hashed_user_password environment file or seed script with the newly generated one:

    ```
    PRE_HASHED_USER_PASSWORD=b'HASHEDPASSWORDHERE'
    ```

### Storing Pre-Hashed Passwords
- **Environment File**: The pre-hashed password should be stored in an environment file named `.env.pre_hashed_user_passwords` (or another appropriately named `.env` file depending on the environment).
- **Environment Variable**: Ensure that the pre-hashed password is assigned to the `PRE_HASHED_USER_PASSWORD` environment variable.
- **Seeding Script**: The seeding script will automatically use the `PRE_HASHED_USER_PASSWORD` environment variable to assign the hashed password to the user records during the seeding process.

### Example Usage in Seeding Script
In your seeding script, the hashed password is fetched from the environment variable like so:

```python
from api.config.config import PRE_HASHED_USER_PASSWORD

def seed_users(session, users):
    for user in users:
        user.hashed_password = PRE_HASHED_USER_PASSWORD
        session.add(user)
    session.commit()
```
### Additional Notes
- Ensure that your `.env` files are properly git-ignored to avoid committing sensitive information to the repository.
- Before pushing changes, verify that the environment and seed data are correctly set up and tested in your local environment.
### NOTE: BOTH DATABASES ARE CURRENTLY SEEDED FROM THE SAME DEVELOPMENT DATA FILE!