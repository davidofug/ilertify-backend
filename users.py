from flask import jsonify,request

from bson.objectid import ObjectId
from db import connect

connection = connect()
db = connection.shineafrika

def getUsers():
    return "Users will be returned"