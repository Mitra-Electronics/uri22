from base64 import b64encode
from pathlib import Path
from secrets import token_bytes

from passlib.context import CryptContext

if (Path(__file__).parent / ".web").exists():
    from config.dev import PEPPER, SCHEMES
else:
    from config.prod import PEPPER, SCHEMES

con = CryptContext(schemes=[SCHEMES], deprecated='auto')


def hash_password(passw: str):
    return con.hash(PEPPER+passw)


def gen_id():
    return b64encode(token_bytes(30), b'gr').decode('utf-8')


def verify_password(passw: str, hashed_passw: str):
    return con.verify(PEPPER+passw, hashed_passw)
