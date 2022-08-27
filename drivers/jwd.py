from datetime import datetime
from pathlib import Path

from fastapi import HTTPException
from jose import JWTError, jwt

if (Path(__file__).parent.parent / ".web").exists():
    from config.dev import ALGORITHM, SECRET_KEY, TOKEN_TIMEOUT
else:
    from config.prod import ALGORITHM, SECRET_KEY, TOKEN_TIMEOUT


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + TOKEN_TIMEOUT
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username
