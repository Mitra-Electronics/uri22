from datetime import timedelta
from os import environ

# MongoDB
MONGODB_URL = environ["MONGODB_URL"]

# Crypto
PEPPER = environ["PEPPER"]
SCHEMES = environ["SCHEMES"]

# JWT
SECRET_KEY = environ["SECRET_KEY"]
ALGORITHM = environ["ALGORITHM"]
TOKEN_TIMEOUT = timedelta(minutes=int(environ["TOKEN_TIMEOUT"]))