# 💕💕💕💕❤️❤️❤️😍😍😍 #
from pymongo import MongoClient
import urllib.parse
from dotenv import load_dotenv

from pathlib import Path
import os
 
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

DB = os.getenv("DB")
USERNAME = urllib.parse.quote_plus(os.getenv("DB_USER"))
PASSWORD = urllib.parse.quote_plus(os.getenv("DB_PASSWORD"))

mongoURL = "mongodb+srv://{}:{}@lesson0.11nbe.gcp.mongodb.net/{}?retryWrites=true&w=majority".format(USERNAME, PASSWORD, DB)

def connect():
    try :
        connection = MongoClient( mongoURL)
        return connection[DB]
    except Exception as e:
        return e