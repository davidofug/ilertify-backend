from pymongo import MongoClient
import urllib.parse

username = urllib.parse.quote_plus('wampamba2')
password = urllib.parse.quote_plus('GQMYagZHto9RovSN')
mongoURL = "mongodb+srv://{}:{}@lesson0.11nbe.gcp.mongodb.net/shineafrika?retryWrites=true&w=majority".format(username, password)

def connect():
    try :
        return MongoClient( mongoURL)
    except Exception as e:
        return e
    
