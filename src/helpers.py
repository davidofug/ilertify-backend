import jwt
from dotenv import load_dotenv
from pathlib import Path
import os
from src.db import connect


load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

def generateToken(payload, type=1):
    if(type == 1):
        ACCESS_SECRET = os.getenv("ACCESS_SECRET")
        encoded_jwt = jwt.encode(payload, ACCESS_SECRET, algorithm="HS256")
        return encoded_jwt
    
    REFRESH_SECRET = os.getenv("REFRESH_SECRET")
    encoded_jwt = jwt.encode(payload, REFRESH_SECRET, algorithm="HS256")
    return encoded_jwt

def verifyToken(token, username, type=1):
    if( type == 1):
        SECRET = os.getenv("ACCESS_SECRET") 
    else:
        SECRET = os.getenv("REFRESH_SECRET") 

    try:
        decoded_jwt = jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return False
    
    if( decoded_jwt.username == username):
        return True

    return False

def refreshTokens(refreshToken) :
    db = connect()
    acces = generateToken({})
    refresh = generateToken({})
    # result = db.members.
    return True

def destroyToken(token):
    return token