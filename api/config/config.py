import os
from dotenv import load_dotenv
import ast
from api.utils.security_utils.password_utils import hash_password


def convert_string_env_var_to_bytes(environnment_varaiable):
# Retrieves a bytes-like string from environment variables 
# and converts it to bytes to create mock databse data
    string = os.getenv(environnment_varaiable)
    if string.startswith("b'") and string.endswith("'"):
        try:
            bytes = ast.literal_eval(string)
            return bytes
        except ValueError:
            raise ValueError("Invalid bytes format in environment variable.")
    else:
        raise ValueError("Environment variable format is not bytes.")


# Load environment based on the current ENV setting
environment = os.getenv('ENV', 'development')
if environment == 'production':
    load_dotenv('.env.production')
else:
    load_dotenv('.env.development')

load_dotenv('.env.pre_hashed_user_password')

# Set environment variables for use in prioject
DATABASE_URL = os.getenv('DATABASE_URL')
PRE_HASHED_USER_PASSWORD = convert_string_env_var_to_bytes(
    'PRE_HASHED_USER_PASSWORD')
