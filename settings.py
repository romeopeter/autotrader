from decouple import config

DEBUG = config("DEBUG", cast=bool)

# TDAmeritrade keys
CLIENT_ID = config("CLIENT_ID", cast=str)
REDIRECT_URI = config("REDIRECT_URI", cast=str)
JSON_PATH = config("JSON_PATH", cast=str)
ACCOUNT_NUMBER = config("ACCOUNT_NUMBER", cast=str)
