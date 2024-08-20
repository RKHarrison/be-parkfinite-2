from fastapi import Depends, HTTPException
from typing import Annotated
from jose import jwt, JWTError
from starlette import status

from api.auth import oauth2_bearer
from api.config.config import SECRET_KEY, ALGORITHM



def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if not username or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        return {'username': username, 'id': user_id}
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Login has expired or is invalid. Please login again.")
