import os
from dotenv import load_dotenv

environment = os.getenv('ENV', 'development')

if environment == 'production':
    load_dotenv('.env.production')
else:
    load_dotenv('.env.development')

load_dotenv('.env.pre_hashed_user_password')

DATABASE_URL = os.getenv('DATABASE_URL')
PRE_HASHED_USER_PASSWORD = os.getenv('PRE_HASHED_USER_PASSWORD')