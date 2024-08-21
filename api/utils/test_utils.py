from datetime import datetime, timedelta
from api.crud.auth_crud import create_access_token


def is_valid_date(date_str):
    if not date_str or type(date_str) != str:
        return False
    try:
        datetime.fromisoformat(date_str)
        return True
    except ValueError:
        return False


def get_test_user_token(test_user_data):
    access_token = create_access_token(user_id=test_user_data['user_id'], username=test_user_data['username'], expires_delta=timedelta(minutes=30))
    return access_token