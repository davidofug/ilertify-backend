import jwt
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

def generateToken(payload):
    SECRET = load_dotenv(os.getenv("SECRET"))
    encoded_jwt = jwt.encode(payload, SECRET, algorithm="HS256")
    return encoded_jwt

def verifyToken(token):
    return status

def destroyToken(token):
    return true